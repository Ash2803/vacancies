"""Simple example usage of terminaltables without any other dependencies.
Just prints sample text and exits.
"""

from __future__ import print_function

from terminaltables import AsciiTable

data = (
    ('Язык программирования',
     'Вакансий найдено',
     'Вакансий обработано',
     'Средняя зарплата'),
)


def main():
    """Main function."""
    title = 'SuperJob Moscow'
    # AsciiTable.
    table_instance = AsciiTable(data, title)
    table_instance.justify_columns[0] = 'center'
    print(table_instance.table)
    print()

    # # SingleTable.
    # table_instance = SingleTable(TABLE_DATA, title)
    # table_instance.justify_columns[2] = 'right'
    # print(table_instance.table)
    # print()
    #
    # # DoubleTable.
    # table_instance = DoubleTable(TABLE_DATA, title)
    # table_instance.justify_columns[2] = 'right'
    # print(table_instance.table)
    # print()


if __name__ == '__main__':
    main()