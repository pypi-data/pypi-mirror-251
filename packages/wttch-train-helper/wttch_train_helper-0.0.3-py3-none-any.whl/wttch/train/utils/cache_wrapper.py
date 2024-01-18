from functools import wraps
import os.path


def cache_wrapper(filename, save_path=None, force_write=True, use='joblib'):
    """
    装饰器，训练完保存模型，如果模型存在则加载。
    :param filename: 保存的文件名
    :param force_write: 强行刷新模型
    :param save_path: 模型保存位置
    """

    # 外层为了获取 save_path 参数
    # wrapper 才是真正的装饰器
    def wrapper(train_func):
        """

        :param train_func: 训练模型的函数
        """

        @wraps(train_func)
        def inner(*args, **kwargs):
            if save_path is not None:
                _try_make_dirs(save_path)
                real_filename = os.path.join(save_path, filename)
            else:
                real_filename = filename
            if force_write or not os.path.exists(real_filename):
                # 强制写入或者没有缓存
                # 执行并保存
                print('开始任务...')
                model = train_func(args, kwargs)
                if use == 'joblib':
                    import joblib
                    joblib.dump(model, filename)
                    print(f'任务完成, 保存{type(model)} -> {save_path} ({use})')
                elif use == 'pickle':
                    import pickle
                    with open(filename, 'rb') as f:
                        pickle.dump(model, f)
                        print(f'任务完成, 保存{type(model)} -> {save_path} ({use})')
                else:
                    raise ValueError(f'未知的保存模型方式{use}')
                return model
            else:
                # 加载
                if use == 'joblib':
                    import joblib
                    return joblib.load(filename)
                if use == 'pickle':
                    import pickle
                    with open(filename, 'rb') as f:
                        return pickle.load(f)

                raise ValueError(f'未知的保存模型方式{use}')

        return inner

    return wrapper


def _try_make_dirs(path):
    if not os.path.exists(path):
        # 创建文件夹
        os.makedirs(path)
        print(f"创建缓存文件夹: {path}")
