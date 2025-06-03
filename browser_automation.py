#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для автоматизации действий в браузере с использованием Playwright.
"""

import asyncio
import logging
import os
import time
from pathlib import Path
from typing import Dict, Any, Optional

import yaml
from playwright.async_api import async_playwright, Page, Browser, BrowserContext, Download

class BrowserAutomation:
    """Класс для автоматизации действий в браузере."""

    def __init__(self, config_path: str = "config.yaml"):
        """
        Инициализация класса.

        Args:
            config_path: Путь к файлу конфигурации
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
        
        # Пути к локальным браузерам
        self.browser_paths = {
            'chromium': str(Path('browsers/chromium/chrome-win').absolute()),
            'firefox': str(Path('browsers/firefox').absolute()),
            'webkit': str(Path('browsers/webkit').absolute())
        }
        
        # Создаем директорию для загрузок, если она не существует
        self.downloads_dir = Path('Downloads')
        self.downloads_dir.mkdir(exist_ok=True)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Загрузка конфигурации из YAML файла.

        Args:
            config_path: Путь к файлу конфигурации

        Returns:
            Dict[str, Any]: Загруженная конфигурация
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _setup_logging(self) -> None:
        """Настройка логирования."""
        log_config = self.config['logging']
        log_params = {
            'encoding': 'utf-8',
            'level': getattr(logging, log_config['level']),
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        }

        if log_config['log_in_file']:
            log_params['filename'] = log_config['file']

        logging.basicConfig(**log_params)
        self.logger = logging.getLogger(__name__)

    async def _wait_for_element(self, selector, timeout: int = 30000) -> None:
        """
        Ожидание появления элемента на странице.

        Args:
            selector: CSS селектор элемента или список селекторов
            timeout: Таймаут ожидания в миллисекундах
        """
        if isinstance(selector, list):
            for sel in selector:
                try:
                    await self.page.wait_for_selector(sel, timeout=timeout)
                    self.logger.info(f"\tЭлемент {sel} успешно загружен")
                    return
                except Exception:
                    continue
            raise Exception(f"Ни один из селекторов {selector} не был найден")
        else:
            await self.page.wait_for_selector(selector, timeout=timeout)
            self.logger.info(f"\tЭлемент {selector} успешно загружен")

    async def click_element(self, selector, wait_for: bool = True) -> None:
        """
        Нажатие на элемент.

        Args:
            selector: CSS селектор элемента или список селекторов
            wait_for: Нужно ли ждать появления элемента
        """
        if wait_for:
            await self._wait_for_element(selector)
        
        if isinstance(selector, list):
            for sel in selector:
                try:
                    await self.page.click(sel)
                    self.logger.info(f"\tВыполнено нажатие на элемент {sel}")
                    return
                except Exception:
                    continue
            raise Exception(f"Не удалось кликнуть ни по одному из селекторов {selector}")
        else:
            await self.page.click(selector)
            self.logger.info(f"\tВыполнено нажатие на элемент {selector}")

    async def input_text(self, selector, text: str, wait_for: bool = True) -> None:
        """
        Ввод текста в поле ввода.

        Args:
            selector: CSS селектор элемента или список селекторов
            text: Текст для ввода
            wait_for: Нужно ли ждать появления элемента
        """
        if wait_for:
            await self._wait_for_element(selector)
        
        if isinstance(selector, list):
            for sel in selector:
                try:
                    await self.page.fill(sel, text)
                    self.logger.info(f"\tВведен текст в элемент {sel}")
                    return
                except Exception:
                    continue
            raise Exception(f"Не удалось ввести текст ни в один из селекторов {selector}")
        else:
            await self.page.fill(selector, text)
            self.logger.info(f"\tВведен текст в элемент {selector}")

    async def _handle_download(self, download: Download) -> None:
        """
        Обработка скачивания файла.

        Args:
            download: Объект загрузки
        """
        try:
            # Получаем имя файла из заголовка Content-Disposition
            filename = download.suggested_filename
            if not filename:
                filename = f"downloaded_file_{int(time.time())}.csv"
            
            # Сохраняем файл в директорию Downloads
            file_path = self.downloads_dir / filename
            await download.save_as(file_path)
            self.logger.info(f"Файл успешно сохранен: {file_path}")
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении файла: {str(e)}")

    async def setup_browser(self) -> None:
        """Инициализация браузера и создание нового контекста."""
        self.playwright = await async_playwright().start()
        
        # Используем локальный путь к браузеру
        executable_path = os.path.join(self.browser_paths['chromium'], 'chrome.exe')
        if not os.path.exists(executable_path):
            self.logger.warning(f"Локальный браузер не найден по пути {executable_path}")
            self.logger.info("Используем браузер из системной установки")
            self.browser = await self.playwright.chromium.launch(headless=False, args=["--start-maximized"])
        else:
            self.logger.info(f"Используем локальный браузер из {executable_path}")
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                executable_path=executable_path,
                args=["--start-maximized"],
            )
            
        # Настраиваем контекст с отключенным автоматическим открытием файлов
        self.context = await self.browser.new_context(
            no_viewport=True,
            accept_downloads=True
        )
        
        # Устанавливаем обработчик загрузок
        self.page = await self.context.new_page()
        self.page.on("download", self._handle_download)
        
        self.logger.info("Браузер успешно инициализирован")

    async def close_browser(self) -> None:
        """Закрытие браузера и освобождение ресурсов."""
        try:
            if self.page:
                await self.page.close()
                self.page = None
            if self.context:
                await self.context.close()
                self.context = None
            if self.browser:
                await self.browser.close()
                self.browser = None
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
            self.logger.info("Все ресурсы успешно освобождены")
        except Exception as e:
            self.logger.error(f"Ошибка при закрытии ресурсов: {str(e)}")

    async def execute_actions(self) -> None:
        """Выполнение последовательности действий из конфигурации."""
        try:
            await self.setup_browser()
            await self.page.goto(self.config['site']['url'])
            self.logger.info(f"Переход на страницу {self.config['site']['url']}")

            for action in self.config['actions']:
                action_type = action['type']
                selector = action['selector']
                wait_for = action.get('wait_for', True)
                description = action.get('description', '')
                timeout = action.get('timeout', None)
                wait = action.get('wait', None)

                self.logger.info(f"Выполнение действия: {description}")

                if wait:
                    await asyncio.sleep(wait)

                if action_type == 'click':
                    await self.click_element(selector, wait_for)
                elif action_type == 'input':
                    value = action['value']
                    # Подстановка значений из конфигурации
                    if isinstance(value, str) and value.startswith('${'):
                        config_path = value[2:-1].split('.')
                        value = self.config
                        for key in config_path:
                            value = value[key]
                    await self.input_text(selector, value, wait_for)

                if timeout:
                    await asyncio.sleep(timeout)

            # Проверяем настройку закрытия браузера
            if self.config['site'].get('close_browser_after_completion', True):
                self.logger.info("Закрытие браузера после выполнения всех действий")
                await self.close_browser()
            else:
                self.logger.info("Браузер оставлен открытым на некоторое время после выполнения всех действий.")
                time.sleep(self.config['other'].get('sleep', 1))
                await self.close_browser()

        except Exception as e:
            self.logger.error(f"Произошла ошибка: {str(e)}")
            raise
        finally:
            # Закрываем браузер только если произошла ошибка
            if self.config['site'].get('close_browser_after_completion', True):
                await self.close_browser()

async def main():
    """Основная функция для запуска автоматизации."""
    automation = BrowserAutomation()
    
    try:
        await automation.execute_actions()
    except Exception as e:
        automation.logger.error(f"Произошла ошибка: {str(e)}")
        await automation.close_browser()

def run():
    """Запуск программы с обработкой ошибок."""
    logger = logging.getLogger(__name__)
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    run()
