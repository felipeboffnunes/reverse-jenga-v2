
def main():
    from setup import setup_parameters
    setup_parameters()
    from timer import Chrono
    Chrono.dialogue_begin()
    Chrono()


if __name__ == '__main__':
    main()
