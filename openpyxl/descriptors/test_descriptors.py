import pytest


class TestDescriptor:

    from . import Descriptor

    class Dummy:
        pass

    def test_ctor(self):
        d = self.Descriptor('key', size=1)
        assert d.name == 'key'
        assert d.size == 1

    def test_setter(self):
        d = self.Descriptor('key')
        client = self.Dummy()
        d.__set__(client, 42)
        assert client.key == 42


@pytest.fixture
def boolean():

    from . import Bool, Strict

    class Dummy(Strict):

        value = Bool()

    return Dummy()


class TestBool:

    def test_valid(self, boolean):
        boolean.value = True
        assert boolean.value

    @pytest.mark.parametrize("value, expected",
                             [
                                 (1, True,),
                                 (0, False),
                                 ('true', True),
                                 ('false', True),
                                 ('', False),
                                 ([], False)
                             ]
                              )
    def test_cast(self, boolean, value, expected):
        boolean.value = value
        assert boolean.value == expected


@pytest.fixture
def integer():

    from . import Integer, Strict

    class Dummy(Strict):

        value =  Integer()

    return Dummy()


class TestInt:

    def test_valid(self, integer):
        integer.value = 4
        assert integer.value == 4

    @pytest.mark.parametrize("value", ['a', '4.5', None])
    def test_invalid(self, integer, value):
        with pytest.raises(TypeError):
            integer.value = value

    @pytest.mark.parametrize("value, expected",
                             [
                                 ('4', 4),
                                 (4.5, 4),
                             ])
    def test_cast(self, integer, value, expected):
        integer.value = value
        assert integer.value == expected


@pytest.fixture
def float():

    from . import Float, Strict

    class Dummy(Strict):

        value =  Float()

    return Dummy()


class TestFloat:

    def test_valid(self, float):
        float.value = 4
        assert float.value == 4

    @pytest.mark.parametrize("value", ['a', None])
    def test_invalid(self, float, value):
        with pytest.raises(TypeError):
            float.value = value

    @pytest.mark.parametrize("value, expected",
                             [
                                 ('4.5', 4.5),
                                 (4.5, 4.5),
                                 (4, 4.0),
                             ])
    def test_cast(self, float, value, expected):
        float.value = value
        assert float.value == expected



@pytest.fixture
def maximum():
    from . import Max, Strict

    class Dummy(Strict):

        value = Max(max=5)

    return Dummy()


class TestMax:

    def test_ctor(self):
        from . import Strict, Max

        with pytest.raises(TypeError):
            class Dummy(Strict):
                value = Max()

    def test_valid(self, maximum):
        maximum.value = 4
        assert maximum.value == 4

    def test_invalid(self, maximum):
        with pytest.raises(ValueError):
            maximum.value = 6


@pytest.fixture
def minimum():
    from . import Min, Strict

    class Dummy(Strict):

        value = Min(min=0)

    return Dummy()


class TestMin:

    def test_ctor(self):
        from . import Strict, Min

        with pytest.raises(TypeError):
            class Dummy(Strict):
                value = Min()


    def test_valid(self, minimum):
        minimum.value = 2
        assert minimum.value == 2


    def test_invalid(self, minimum):
        with pytest.raises(ValueError):
            minimum.value = -1


@pytest.fixture
def min_max():
    from . import MinMax, Strict

    class Dummy(Strict):

        value = MinMax(min=-1, max=1)

    return Dummy()


class TestMinMax:

    def test_ctor(self):
        from . import MinMax, Strict

        with pytest.raises(TypeError):

            class Dummy(Strict):
                value = MinMax(min=-10)

        with pytest.raises(TypeError):

            class Dummy(Strict):
                value = MinMax(max=10)


    def test_valid(self, min_max):
        min_max.value = 1
        assert min_max.value == 1


    def test_invalid(self, min_max):
        with pytest.raises(ValueError):
            min_max.value = 2


@pytest.fixture
def set():
    from . import Set, Strict

    class Dummy(Strict):

        value = Set(values=[1, 'a', None])

    return Dummy()


class TestValues:

    def test_ctor(self):
        from . import Set, Strict

        with pytest.raises(TypeError):
            class Dummy(Strict):

                value = Set()


    def test_valid(self, set):
        set.value = 1
        assert set.value == 1


    def test_invalid(self, set):
        with pytest.raises(ValueError):
            set.value = 2


@pytest.fixture
def ascii():

    from . import ASCII, Strict

    class Dummy(Strict):

        value = ASCII()

    return Dummy()


class TestASCII:

    def test_valid(self, ascii):
        ascii.value = 'some text'
        assert ascii.value == 'some text'.encode("ascii")

    value = '\xc3\xbc'
    try:
        value = value.decode("utf8")
    except AttributeError:
        pass
    @pytest.mark.parametrize("value",
                             [
                                 value,
                                 10,
                                 []
                             ]
                             )
    def test_invalid(self, ascii, value):
        with pytest.raises(TypeError):
            ascii.value = value


@pytest.fixture
def string():

    from . import String, Strict

    class Dummy(Strict):

        value = String()

    return Dummy()


class TestString:

    def test_valid(self, string):
        value = '\xc3\xbc'
        try:
            value = value.decode("utf-8")
        except AttributeError:
            pass
        string.value = value
        assert string.value == value

    def test_invalid(self, string):
        with pytest.raises(TypeError):
            string.value = 5
