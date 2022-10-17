import logging as log 

log.basicConfig(level=log.INFO,
                format = '%(asctime)s: %(levelname)s [%(filename)s: %(lineno)s] %(message)s',
                datefmt = '%I:%M:%S %p',
                handlers=[
                    log.FileHandler("tele_bot.log"),
                    log.StreamHandler()
                ])

if __name__ == "__main__":
    log.debug("Mensaje a nivel de debug")
    log.info("Mensaje a nivel de info")
    log.warning("Mensaje a nivel de peligro")
    log.error("Mensaje a nivel de error")
    log.critical("Mensaje a nivel critico")
