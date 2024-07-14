import asyncio
import aiofiles
import os
from aiohttp import ClientSession
from pathlib import Path
from argparse import ArgumentParser
import logging

# Have to be installed:
#    python -m venv venv                         # Створення віртуального середовища
#    Set-ExecutionPolicy Bypass -Scope Process   # змінити політику виконання для поточної сесії PowerShell (без цього не дає активувати)      
#    .\venv\Scripts\activate
#    pip install aiohttp
#    pip install aiofiles

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def read_folder(source_folder, output_folder):
    for root, _, files in os.walk(source_folder):
        tasks = []
        for file in files:
            source_path = Path(root) / file
            tasks.append(copy_file(source_path, output_folder))
        await asyncio.gather(*tasks)

async def copy_file(source_path, output_folder):
    try:
        ext = source_path.suffix[1:]  # Отримуємо розширення файлу без крапки
        if not ext:
            ext = 'no_extension'
        dest_folder = Path(output_folder) / ext
        dest_folder.mkdir(parents=True, exist_ok=True)
        dest_path = dest_folder / source_path.name
        
        async with aiofiles.open(source_path, 'rb') as fsrc:
            async with aiofiles.open(dest_path, 'wb') as fdst:
                await fdst.write(await fsrc.read())
                
        logger.info(f"Copied {source_path} to {dest_path}")
    except Exception as e:
        logger.error(f"Error copying {source_path}: {e}")

async def main():
    
    parser = ArgumentParser(description="Sort files by extension asynchronously.")    
    # Parce source_folder and output_folder from command prompt:
    parser.add_argument('source_folder', type=str, help='Source folder to read files from.')
    parser.add_argument('output_folder', type=str, help='Destination folder to copy files to.')

    ## For set source_folder and output_folder like default:
    # parser.add_argument('source_folder', type=str, nargs='?', default='C://path/to/default/source_folder', help='Source folder to read files from.')
    # parser.add_argument('output_folder', type=str, nargs='?', default='C://output_folder', help='Destination folder to copy files to.')

    args = parser.parse_args()
    source_folder = args.source_folder
    output_folder = args.output_folder
    
    await read_folder(source_folder, output_folder)

if __name__ == '__main__':
    asyncio.run(main())