def func():
    print("__name__ = {}".format(__name__))
    print("function is working")

if __name__ == "__main__":
    print("직접 실행")
    print(__name__)

else:
    print("임포트되어 실행")
    print(__name__)
