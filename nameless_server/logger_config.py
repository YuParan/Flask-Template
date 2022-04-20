def get_logging_config(project_name, log_dir):
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'stack_info': True,
                'format':
                    '[%(levelname)s]  '
                    '%(process)d:%(processName)s  '
                    '%(asctime)s  '
                    '%(pathname)s:%(lineno)s  '
                    '%(funcName)s()  '
                    '%(message)s  '
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'standard'
            },
            'debug': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': f'{log_dir}/{project_name}-debug.log',
                'maxBytes': 1024 * 1024 * 8,
                'backupCount': 5,
                'formatter': 'standard',
            },
            'request_handler': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': f'{log_dir}/request.log',
                'maxBytes': 1024 * 1024 * 8,
                'backupCount': 5,
                'formatter': 'standard',
            }
        },
        # 'loggers': {
        #     f'{project_name}': {
        #         'handlers': ['console', 'wsgi', 'debug', 'request_handler'],
        #         'level': 'DEBUG',
        #         'propagate': False
        #     },
        #     'werkzeug': {
        #         'handlers': ['console', 'wsgi', 'request_handler'],
        #         'level': 'DEBUG',
        #         'propagate': False
        #     }
        # },
        'root': {
            'handlers': ['console', 'debug', 'request_handler'],
            'level': 'DEBUG'
        }
    }
