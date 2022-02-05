# import io
# import sys
# import time
# import threading
#
#
# class ThreadWithResult(threading.Thread):
#     def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
#         def function():
#             self.result = target(*args, **kwargs)
#
#         super().__init__(group=group, target=function, name=name, daemon=daemon)
#
#
# def get_input():
#     time.sleep(1)
#     a = input(":")
#     print(f"{a}, it printed")
#
#
# def write_input():
#     sin = io.StringIO()
#     sys.stdin = sin
#     ret = sin.getvalue()
#     return ret
#
#
# if __name__ == '__main__':
#     t1 = ThreadWithResult(target=get_input)
#     t2 = ThreadWithResult(target=write_input)
#
#     t1.start()
#     t2.start()
#
#     t1.join()
#     t2.join()
#     print(f"reached, {t2.result}")


new = """
a = input(":")
b = input(":")
print(a, b)
"""

exec(new)
