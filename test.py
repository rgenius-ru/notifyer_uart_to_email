import configparser

config_file_name = 'config.ini'
config = configparser.ConfigParser()
print(config.sections)

config.read(config_file_name)

if not config:
    print(f"File {config_file_name} not found")

print(config)
print(config.sections)

# for candidate in ['smtp_server', 'port', 'sender_email', 'password']:
#     print('%-12s: %s' % (candidate, parser.has_section(candidate)))

# parser.get('email', )
