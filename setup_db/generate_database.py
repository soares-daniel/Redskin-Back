import alembic.config

def generate_database():
    alembic_args = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembic_args)

if __name__ == '__main__':
    generate_database()
