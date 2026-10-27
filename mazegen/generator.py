# class

def generate(self) -> list[list[int]]:
    self._grid = [[0xF] * self._width for _ in range(self._height)]
    self._place_pattern()
    self._carve_perfect()
    if not self._perfect:
        self._braid()
    self._validate()
    return self._grid
