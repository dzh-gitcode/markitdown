import subprocess
import os

# 清理旧的构建
subprocess.run(['Remove-Item', '-Recurse', '-Force', 'dist', 'build', '-ErrorAction', 'SilentlyContinue'], shell=True)

# 创建打包命令
cmd = [
    'pyinstaller',
    '--windowed',
    '--name', 'MarkItDown-GUI',
    '--distpath', 'e:\\markitdown-0.1.6\\dist',
    '--workpath', 'e:\\markitdown-0.1.6\\build',
    '--specpath', 'e:\\markitdown-0.1.6',
    '--exclude-module', 'matplotlib',
    '--exclude-module', 'scipy',
    '--exclude-module', 'PyQt5',
    '--exclude-module', 'tensorflow',
    '--exclude-module', 'torch',
    '--exclude-module', 'sklearn',
    '--exclude-module', 'scikit-image',
    '--exclude-module', 'IPython',
    '--exclude-module', 'notebook',
    '--exclude-module', 'zmq',
    '--exclude-module', 'gevent',
    '--exclude-module', 'twisted',
    '--exclude-module', 'sphinx',
    '--exclude-module', 'sqlalchemy',
    '--exclude-module', 'tables',
    '--exclude-module', 'vtk',
    '--exclude-module', 'dask',
    '--exclude-module', 'distributed',
    '--exclude-module', 'cv2',
    '--exclude-module', 'imageio',
    '--exclude-module', 'dlib',
    '--exclude-module', 'cloudpickle',
    '--exclude-module', 'nltk',
    '--exclude-module', 'networkx',
    '--exclude-module', 'numba',
    '--exclude-module', 'llvmlite',
    '--exclude-module', 'xarray',
    '--exclude-module', 'pytest',
    'markitdown-gui-final.py'
]

print("开始打包...")
result = subprocess.run(' '.join(cmd), shell=True, capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("返回码:", result.returncode)