import configparser

pc_str = '[PC program Config parser]'

config_filename = 'config.ini'
section_email = 'email'
options = ['smtp_server', 'port', 'sender_email', 'password']

config = configparser.ConfigParser()

if not config.read(config_filename):
    assert f"Can not read file: {config_filename}"

print(pc_str, 'Found config sections:', config.sections())

stop_flag = False
for option in options:
    has = config.has_option(section_email, option)

    if not has:
        stop_flag = True
        value = '*** Error Option ***'
    else:
        value = config.get(section_email, option)

    print(pc_str, '%-12s: %s' % (option, value))

if stop_flag:
    print(f"\nCan not read all options in section [{section_email}]")
    exit(1)


smtp_server = config.get(section_email, 'smtp_server')
port = config.get(section_email, 'port')
sender_email = config.get(section_email, 'sender_email')
password = config.get(section_email, 'password')


if __name__ == "__main__":
    pass
