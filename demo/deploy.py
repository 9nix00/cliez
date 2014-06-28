# -*- coding: utf-8 -*-

from codez.deploy.base.config import Template


config={
    # allow list or string
    # if is string,treate it as pssh group. default path is $HOME/.dsh/group, you can use `--root'
    'machines': ['root@10.1.22.4'],
    'service': [
        'nginx',
        'tornado'
    ],
    'nginx': {
        'upstream': {
            'name': 'kbonez',
            'user':'nobody',
            'servers': [
                '127.0.0.1:9000',
                '127.0.0.1:9001',
                '127.0.0.1:9002',
                '127.0.0.1:9003',
                '127.0.0.1:9004',
                '127.0.0.1:9005',
                '127.0.0.1:9006',
                '127.0.0.1:9007',
                '127.0.0.1:9008',
                '127.0.0.1:9009',
            ],
        },
        'server': [
            {
                'variable': {
                    'name': 'www.example.com',
                },
                'template': Template.Nginx.upstream
            },
            {
                'variable': {
                    'name': 'www.example.com',
                },
                'template': Template.Nginx.php
            }
        ],
    },
    'tornado':{
        'start_port':9000,
        'process':10,
    }

}



