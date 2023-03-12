class TextFormater:
    def channel_post(self, text: str):
        final_text = f'CHANNEL POST\n{text.capitalize()}\nEnd post'
        return final_text
