"""
Made by Mathieu Marquis, January 16th 2024.
"""

class Colors():
    """
    Homemade class to integrate colors easier.
    """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

    def __str__(self):
        return (
            f"\n{self.BOLD}{self.UNDERLINE}LIST OF ALL COLORS{self.END}\n" +
            f"{self.BLACK}BLACK{self.END}\n"
            f"{self.RED}RED{self.END}\n"
            f"{self.GREEN}GREEN{self.END}\n"
            f"{self.BROWN}BROWN{self.END}\n"
            f"{self.BLUE}BLUE{self.END}\n"
            f"{self.PURPLE}PURPLE{self.END}\n"
            f"{self.CYAN}CYAN{self.END}\n"
            f"{self.LIGHT_GRAY}LIGHT_GRAY{self.END}\n"
            f"{self.DARK_GRAY}DARK_GRAY{self.END}\n"
            f"{self.LIGHT_RED}LIGHT_RED{self.END}\n"
            f"{self.LIGHT_GREEN}LIGHT_GREEN{self.END}\n"
            f"{self.YELLOW}YELLOW{self.END}\n"
            f"{self.LIGHT_BLUE}LIGHT_BLUE{self.END}\n"
            f"{self.LIGHT_PURPLE}LIGHT_PURPLE{self.END}\n"
            f"{self.LIGHT_CYAN}LIGHT_CYAN{self.END}\n"
            f"{self.LIGHT_WHITE}LIGHT_WHITE{self.END}\n"
            f"{self.BOLD}BOLD{self.END}\n"
            f"{self.FAINT}FAINT{self.END}\n"
            f"{self.ITALIC}ITALIC{self.END}\n"
            f"{self.UNDERLINE}UNDERLINE{self.END}\n"
            f"{self.BLINK}BLINK{self.END}\n"
            f"{self.NEGATIVE}NEGATIVE{self.END}\n"
            f"{self.CROSSED}CROSSED{self.END}\n"
            f"{self.END}END{self.END}\n"
        )

    def help(self):
        return ("\nIf multiple formats are used, the color should be inserted first. A string should always end with "+
              f"{Colors.BOLD}COLORS.END{Colors.END} when doing multiple prints.\n"+
              f"See print(Colors()) to get a list of all color codes.\n")
