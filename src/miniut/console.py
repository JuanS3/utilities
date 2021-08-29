from typing import List, Union
import functools
import platform
import os
import colorama

from miniut import config as cfg


COLORS_LIST = [RED     := 'RED',
               GREEN   := 'GREEN',
               YELLOW  := 'YELLOW',
               BLUE    := 'BLUE',
               MAGENTA := 'MAGENTA',
               CYAN    := 'CYAN',
               ]

__COLORS = {RED     : colorama.Fore.RED,
            GREEN   : colorama.Fore.GREEN,
            YELLOW  : colorama.Fore.YELLOW,
            BLUE    : colorama.Fore.BLUE,
            MAGENTA : colorama.Fore.MAGENTA,
            CYAN    : colorama.Fore.CYAN
            }

__indentation_type  : str = ' '
__indentation_lvl   : str = ''
__indentantion_size : int = 2
__is_init : bool = False


__START_LANGS = {cfg.ENG : 'START',
                 cfg.ESP : 'INICIA',
                 }

__END_LANGS = {cfg.ENG : 'END',
               cfg.ESP : 'TERMINA',
               }


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                         decorators                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def block(message_block: Union[str, dict], color: str = BLUE):
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            message = message_block
            if isinstance(message_block, dict):
                message = message_block[cfg.lang()]

            start_block(message, color)
            new_line()
            value = func(*args, **kwargs)
            new_line()
            end_block(message, color)
            return value
        return wrapped
    return decorator


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                          functions                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def __init():
    """
    If the console still doesn't start, then start the console without
    clearing the screen, but do nothing if the console is started
    """
    if not __is_init:
        init(False)


def init(clear: bool = True, indentation_type: str = ' ', indentation_size: int = 2):
    """
    Initialize the console, and resert the indentation level

    Parameters
    ----------
    clear : bool, optional
        True to clear the screen and False is not, by default True
    """
    global __is_init, __indentation_lvl, __indentantion_size, __indentation_type
    __indentation_lvl = ''
    __indentantion_size = indentation_size
    __indentation_type  = indentation_type

    colorama.init(autoreset=True)
    if clear:
        clear_screen()
    __is_init = True


def clear_screen():
    """
    Clear the console screen
    """
    os.system('clear' if platform.system() != 'Windows' else 'cls')


def add_lvl():
    """
    Add one level (indentation)
    """
    global __indentation_lvl
    __indentation_lvl += (__indentation_type * __indentantion_size)


def del_lvl():
    """
    Substract one level (indentation)
    """
    global __indentation_lvl
    __indentation_lvl = __indentation_lvl[:-__indentantion_size]


def println(*message: tuple,
            endl: str = '\n',
            withlvl: bool = True,
            color: str = ''
            ) -> None:
    """
    Print the message to the console, the `endl` is the same as `end` in print function
    and is necessary print the message with the current indentation level and the color
    indicate.

    Parameters
    ----------
    message : tuple
        Message to print to console

    endl : str, optional
        The end of line, by default `\\n`

    withlvl : bool, optional
        True if the message should be printed with the current indentation
        False is not necessary, by default `True`

    color : str, optional
        The color of the message, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color
    """
    __init()
    message = __to_string(*message)

    if withlvl: message = __indentation_lvl + message

    if color in COLORS_LIST: msg_col = f'{colorama.Style.BRIGHT}{__COLORS[color]}'
    else: msg_col = ''

    print(f'{msg_col}{message}', end=endl)


def __to_string(*values: tuple, sep: str = ' ') -> str:
    return sep.join([str(m) for m in values])


def start_block(*message: tuple, color: str = BLUE) -> None:
    """
    Start a block of messages

    Parameters
    ----------
    message : tuple
        The title of the block

    color : str, optional
        The color of the title block, by default BLUE
    """
    message = __to_string(*message)
    println(f'{colorama.Style.BRIGHT}{__COLORS[color]}{__START_LANGS[cfg.lang()]} {message.upper()}')
    add_lvl()


def end_block(*message: tuple, color: str = BLUE) -> None:
    """
    End a block of messages

    Parameters
    ----------
    message : tuple
        The title of the block

    color : str, optional
        The color of the title block, by default BLUE
    """
    message = __to_string(*message)
    del_lvl()
    println(f'{colorama.Style.BRIGHT}{__COLORS[color]}{__END_LANGS[cfg.lang()]} {message.upper()}')
    new_line()


def warning(*message: tuple) -> None:
    """
    Warning message starts with 'warning: {message}'

    Parameters
    ----------
    message : tuple
        The message to display in the log
    """
    message = __to_string(*message)
    println(f'{colorama.Style.BRIGHT}{__COLORS[YELLOW]}warning: {message}')


def error(*message: tuple) -> None:
    """
    Error message is displayed like `error: >>> {message} <<<`

    Parameters
    ----------
    message : tuple
        The message to display in the log
    """
    message = __to_string(*message)
    println(f'{colorama.Style.BRIGHT}{__COLORS[RED]}error: >>> {message} <<<')


def new_line():
    """
    Display a blank line in the console
    """
    println('', withlvl=False)


def line(size: int = 30) -> None:
    """
    Display a line in the console like this `-- -- -- -- -- -- --`
    whit the indicated size

    Parameters
    ----------
    size : int, optional
        The size of the line to display, by display 30
    """
    println(f'{("-- " * size)[:-1]}')
    new_line()


def __max_len_value(matrix, nan_format) -> int:

    def max_value(cell) -> int:
        cellstr = str(cell)
        if cellstr in ('None', 'nan', 'NaN'):
            cellstr = nan_format
        return max(max_len, len(cellstr))

    max_len = 0
    for row in matrix:
        if isinstance(row, list):
            for col in row:
                max_len =max_value(col)
        else:
            max_len = max_value(row)
    return max_len


def __print_matrix_header(header: List[str],
                          len_index: int,
                          color_index: str,
                          extra_spacing: str,
                          withlvl: bool,
                          max_len_value: int
                          ) -> None:
    """
    Print the header of the matrix

    Parameters
    ----------
    header : List[str]
        If the matrix has a header to print with them, by default None

    len_index : int
        Longest value size index of the indexes

    color_index : str
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available

    extra_spacing : str
        The extra spacing befote printing the header

    withlvl : bool
        True if the matrix should be printed with the current indentation False in otherwise

    max_len_value : int
        Longest value size in the matrix
    """
    spaces: str = ' ' * (len_index + 3)
    indentation: str = __indentation_lvl if withlvl else ''

    println(f'{indentation}{spaces}{extra_spacing}', endl='', withlvl=False)
    for h in header:
        println(f' {h : ^{max_len_value}} ', color=color_index, endl='', withlvl=False)
    new_line()


def __print_matrix_box_style(matrix,
                             header: List[str],
                             indexes: Union[List[str], str],
                             nan_format: str,
                             color: str,
                             color_index: str,
                             color_style: str,
                             max_len_value: int,
                             len_index: int,
                             style : str,
                             withlvl: bool
                             ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    style : str, optional
        The style to print the matrix, by default `box`
        - `box` Borders around the matrix
        - `semibox` Borders at the top and left of the matrix

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """

    index_row_id = 0
    div: str = '-' * (len(matrix[0]) * max_len_value) + '-' * (len(matrix[0]) * 2)
    spaces: str = ' ' * (len_index + 3)
    indentation: str = __indentation_lvl if withlvl else ''

    if header is not None:
        __print_matrix_header(header = header,
                              len_index = len_index,
                              color_index = color_index,
                              extra_spacing = '',
                              withlvl = withlvl,
                              max_len_value = max_len_value
                              )

    println(f'{indentation}{spaces}{div}', color=color_style, withlvl=False) # printing the bar div

    for row in matrix:
        println(indentation, endl='', withlvl=False)
        if indexes is not None:
            println(f'{indexes[index_row_id]: >{len_index}}', endl='', color=color_index, withlvl=False)
        println(' | ', endl='', color=color_style, withlvl=False)
        index_row_id += 1

        for cell in row:
            cellstr = str(cell) if str(cell) not in ('None', 'nan', 'NaN', '') else nan_format
            println(f' {cellstr : ^{max_len_value}} ', color=color, endl='', withlvl=False)

        if style == 'box':
            println(' | ', color=color_style, withlvl=False)
        else:
            new_line()

    if style == 'box':
        println(f'{indentation}{spaces}{div}', color=color_style, withlvl=False) # printing the bar div
    else:
        new_line()


def __print_matrix_numpy_style(matrix,
                               header: List[str],
                               indexes: Union[List[str], str],
                               style: str,
                               nan_format: str,
                               color: str,
                               color_index: str,
                               color_style: str,
                               max_len_value: int,
                               len_index: int,
                               withlvl: bool
                               ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    index_row_id = 0
    spaces: str = ' ' * (len_index + 3)
    indentation: str = __indentation_lvl if withlvl else ''

    if header is not None:
        __print_matrix_header(header = header,
                              len_index = len_index,
                              color_index = color_index,
                              extra_spacing = '   ',
                              withlvl = withlvl,
                              max_len_value = max_len_value
                              )

    max_rows: int = len(matrix)

    for row in matrix:
        # string line
        if index_row_id == 0:
            println(indentation, '[ ', endl='', color=color_style, withlvl=False)
        else:
            println('  ', indentation, endl='', withlvl=False)

        # index line value
        if indexes is not None:
            println(f'{indexes[index_row_id]: >{len_index}}', endl='', color=color_index, withlvl=False)
        println(' [ ', endl='', color=color_style, withlvl=False)
        index_row_id += 1

        # Line values
        for cell in row:
            cellstr = str(cell) if str(cell) not in ('None', 'nan', 'NaN', '') else nan_format
            println(f' {cellstr : ^{max_len_value}} ', color=color, endl='', withlvl=False)

        # Ending line
        end_line: str = ' ]'
        if max_rows == index_row_id:
            end_line += '  ]'
        println(end_line, color=color_style, withlvl=False)


def __print_matrix_without_style(matrix,
                                 header: List[str] = None,
                                 indexes: Union[List[str], str] = 'all',
                                 style: str = 'box',
                                 nan_format: str = '',
                                 color: str = None,
                                 color_index: str = '',
                                 color_style: str = '',
                                 withlvl: bool = True
                                 ) -> None:
    pass


def print_matrix(matrix,
                 header: List[str] = None,
                 indexes: Union[List[str], str] = 'all',
                 style: str = 'box',
                 nan_format: str = '',
                 color: str = None,
                 color_index: str = '',
                 color_style: str = '',
                 withlvl: bool = True
                 ) -> None:
    """
    Print a matrix in a pretty formatted

    >>> matrix = [[1, 2, 3], [4, 5, 6]]
    >>> print_matrix(matrix)
    ...
    ...     0  1  2
    ...     -------
    ... 0 | 1  2  3 |
    ... 1 | 4  5  6 |
    ...     -------

    >>> print_matrix(matrix,
    >>>              header=['one', 'two', 'three'],
    >>>              indexes=['row1', 'row2'],
    >>>              style='semibox'
    >>>              )
    ...
    ...          one     two    three
    ...        -----------------------
    ... row1 |    1       2       3
    ... row2 |    4       5       6

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    style : str, optional
        The style to print the matrix, by default `box`
        - `box` Borders around the matrix
        - `semibox` Borders at the top and left of the matrix
        - `None` Without borders, only show the values
        - `numpy` or `np` Has been printed like a NumPy matrix

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    indexes_condition = indexes

    if isinstance(indexes_condition, str):
        if indexes_condition in ('all', 'row'):
            indexes = [str(i) for i in range(len(matrix))]

        if indexes_condition in ('all', 'col') and header == None:
            header = [str(i) for i in range(len(matrix[0]))]

        if isinstance(indexes, str):
            indexes = None

    max_len_value = __max_len_value(matrix, nan_format)
    max_len_value = max(max_len_value, __max_len_value([] if header is None else header, nan_format))

    len_index = 0

    if isinstance(indexes, list):
        len_index: int = __max_len_value(indexes, nan_format)

    kwargs = {'matrix' : matrix,
              'header' : header,
              'indexes' : indexes,
              'nan_format' : nan_format,
              'color' : color,
              'color_index' : color_index,
              'color_style' : color_style,
              'max_len_value' : max_len_value,
              'len_index' : len_index,
              'style' : style,
              'withlvl' : withlvl
              }

    if style is None:
        __print_matrix_without_style(**kwargs)
    elif style in ('box', 'semibox'):
        __print_matrix_box_style(**kwargs)
    elif style in ('numpy', 'np'):
        __print_matrix_numpy_style(**kwargs)
