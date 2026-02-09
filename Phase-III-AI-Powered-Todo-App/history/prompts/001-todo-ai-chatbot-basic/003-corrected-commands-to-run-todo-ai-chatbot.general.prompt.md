---
id: 003
title: Corrected Commands to Run Todo AI Chatbot
stage: general
date: 2026-02-07
surface: agent
model: gemini
feature: 001-todo-ai-chatbot-basic
branch: 001-todo-ai-chatbot-basic
user: Aashra Saleem
command: poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
INFO:     Will watch for changes in these directories: ['E:\Projects\Evolution-of-Todo-Hackathon\Phase-III-AI-Powered-Todo-App\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [20000] using WatchFiles
Process SpawnProcess-1:
Traceback (most recent call last):
  File "C:\Python314\Lib\multiprocessing\process.py", line 320, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "C:\Python314\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Me\AppData\Local\pypoetry\Cache\virtualenvs\backend-nOVqSKxe-py3.14\Lib\site-packages\uvicorn\_subprocess.py", line 78, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\Me\AppData\Local\pypoetry\Cache\virtualenvs\backend-nOVqSKxe-py3.14\Lib\site-packages\uvicorn\server.py", line 62, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python314\Lib\asynciounners.py", line 204, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "C:\Python314\Lib\asynciounners.py", line 127, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "C:\Python314\Lib\asyncio\base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "C:\Users\Me\AppData\Local\pypoetry\Cache\virtualenvs\backend-nOVqSKxe-py3.14\Lib\site-packages\uvicorn\server.py", line 69, in serve
    config.load()
    ~~~~~~~~~~~^^
  File "C:\Users\Me\AppData\Local\pypoetry\Cache\virtualenvs\backend-nOVqSKxe-py3.14\Lib\site-ackages\uvicorn\config.py", line 458, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "C:\Users\Me\AppData\Local\pypoetry\Cache\virtualenvs\backend-nOVqSKxe-py3.14\Lib\site-packages\uvicorn\importer.py", line 24, in import_from_string
    raise exc from None
  File "C:\Users\Me\AppData\Local\pypoetry\Cache\virtualenvs\backend-nOVqSKxe-py3.14\Lib\site-packages\uvicorn\importer.py", line 21, in import_from_string
    module = importlib.import_module(module_str)
  File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1398, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 762, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "E:\Projects\Evolution-of-Todo-Hackathon\Phase-III-AI-Powered-Todo-App\backend\main.py", line 6, in <module>
    from backend.src.models.todo import Todo
ModuleNotFoundError: No module named 'backend'
