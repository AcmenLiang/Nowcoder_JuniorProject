# -*- encoding=UTF-8 -*-
# 文件功能：web服务器运行写在这个文件。

from nowstagram import app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
