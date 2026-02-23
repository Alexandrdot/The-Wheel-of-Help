class RatingConverter:
    regex = '[0-5](\.[0-9])?'  # рейтинг от 0 до 5 с десятыми

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)
