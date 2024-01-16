import os
import re
from urllib.parse import unquote
from tqdm import tqdm
import aiohttp


def isNone(x):
    return True if type(x) == type(None) else False

def isFile(fn):
    return True if os.path.isfile(fn) else False

def validate(apikey):
    try:
        return re.match(
            '^([0-9a-fA-F]{8})-([0-9a-fA-F]{4})-([0-9a-fA-F]{4})-([0-9a-fA-F]{4})-([0-9a-fA-F]{12})$',
            apikey)
    except:
        return False

def get_file_from_content_disposition(content_disposition):
    _, params = content_disposition.split(';')
    for param in params.split(';'):
        name, value = param.strip().split('=')
        if name == 'filename':
            filename = unquote(value)
            return filename.rsplit('.', 1)

async def fetch_with_progress(url, header, path, chunk_size=1024):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header) as resp:
            total = int(resp.headers.get('Content-Length', 0))
            if total == 0 and resp.headers.get('Content-Range'):
                match = re.match(r'bytes \d+-\d+/(\d+)', resp.headers['Content-Range'])
                if match:
                    total = int(match.group(1))

            if resp.headers.get('Content-Disposition'):
                name, ext = get_file_from_content_disposition(resp.headers['Content-Disposition'])
            else:
                raise Exception('Invalid content-disposition')
            file_path = f'{path.rstrip("/")}/{name}.{ext}'
            count = 1
            while not isNone(file_path) and isFile(file_path):
                file_path = f'{path.rstrip("/")}/{name}({count}).{ext}'
                count += 1

            with open(file_path, 'wb') as file, tqdm(
                desc=file_path,
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                while True:
                    chunk = await resp.content.read(chunk_size)
                    if not chunk:
                        break
                    size = file.write(chunk)
                    bar.update(size)