import configparser

pc_str = '[PC program Config parser]'

config_filename = 'config.ini'

section_email = 'email'
options_email = ['smtp_server', 'smtp_port', 'sender_email', 'password', 'send_interval']

section_microcontroller = 'microcontroller'
options_serial_port = ['serial_port']

config_structure = {
    section_email: options_email,
    section_microcontroller: options_serial_port
}

config = configparser.ConfigParser()


def check_config_file(filename, structure):
    if not config.read(filename):
        assert f"Can not read file: {filename}"

    print(pc_str, 'In', filename, 'Found config sections:', config.sections())

    stop_flag = False
    for section in structure.keys():
        print()
        print(pc_str, section, ':')
        for option in structure.get(section):
            has = config.has_option(section, option)

            if not has:
                stop_flag = True
                value = '*** Error Option ***'
            else:
                value = config.get(section, option)

            print(pc_str, '  %-14s: %s' % (option, value))

    if stop_flag:
        print(f"\nCan not read all options in section [{section_email}]")
        exit(1)

    print()


check_config_file(config_filename, config_structure)

smtp_server = config.get(section_email, 'smtp_server').strip()
smtp_port = config.getint(section_email, 'smtp_port')
sender_email = config.get(section_email, 'sender_email').strip()
password = config.get(section_email, 'password').strip()
error_send_interval = config.getint(section_email, 'send_interval')

serial_port = config.get(section_microcontroller, 'serial_port')


if __name__ == "__main__":
    pass
