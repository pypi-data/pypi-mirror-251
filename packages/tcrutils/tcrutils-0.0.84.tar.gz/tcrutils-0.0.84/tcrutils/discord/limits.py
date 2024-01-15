class DiscordLimits:
  class Message:
    LENGTH = 4000
    LENGTH_SAFE = 1950
    LENGTH_SAFEST = 1800
    FILE_SIZE_MB = 25

  class Embed:
    TITLE = 256
    DESCRIPTION = 4096
    AUTHOR_NAME = 256

    class Fields:
      AMOUNT = 25
      TITLE = 256
      DESCRIPTION = 1024

    FOOTER = 2048
    TOTAL_CHARACTERS = 6000
