import logging

APP = "camera-ogranizer"

formatter = logging.Formatter("[%(levelname)s] %(message)s")

handler = logging.StreamHandler()
handler.setFormatter(formatter)

log = logging.getLogger(APP)
log.setLevel(logging.INFO)
log.addHandler(handler)
