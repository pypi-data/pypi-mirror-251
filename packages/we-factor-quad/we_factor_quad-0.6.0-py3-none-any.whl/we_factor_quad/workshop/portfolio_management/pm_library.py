import numpy as np
from scipy.optimize import minimize


def square_error(exposures, init_weights, add_idx, add_weights, sigma_f):
    """
    计算加/减仓前后因子暴露的square error
    :param exposures: 当前风格和行业暴露
    :param init_weights: list格式，当前持仓个股的金额权重向量，总权重为 1
    :param add_idx: list格式，元素是init_weights中的index
    :param add_weights: list格式，元素是要加仓的个股权重向量
    :param sigma_f:
    :return:
    """
    assert len(add_idx) == len(add_weights), "add_idx/add_weights does not match"
    assert max(add_idx) < len(init_weights), "add_idx/init_weights does not match"

    add_weights = list(add_weights)
    add_idx = list(add_idx)
    new_weights = list(init_weights).copy()
    total_weights = 1 + sum(add_weights)
    for i in range(len(add_idx)):
        new_weights[add_idx[i]] += add_weights[i]
    init_w = np.array(init_weights)
    new_w = np.array(new_weights) / total_weights
    diff_beta = 100 * (init_w.dot(exposures) - new_w.dot(exposures))
    return (diff_beta.T.dot(sigma_f.dot(diff_beta))).sum()


def in_optimization(df_exposure, df_sigma, code_col, current_values, add_assets, add_value):
    """
    加仓优化函数
    :param df_exposure: 股票因子暴露的数据表格
    :param df_sigma:
    :param code_col: 股票代码列
    :param current_values: 字典格式，当前持仓金额，key是股票代码，value是持仓金额
    :param add_assets: list格式，要加仓的候选股票代码
    :param add_value: float格式，要加仓的总金额
    :return: 字典，key是要加仓的个股代码，value是要加仓的金额
    """

    total_value = sum(current_values.values()) + add_value
    add_weight = total_value / (total_value - add_value) - 1

    all_assets_set = set([])
    for asset in current_values:
        all_assets_set.add(asset)
    for asset in add_assets:
        all_assets_set.add(asset)
    df = df_exposure[df_exposure[code_col].isin(all_assets_set)]
    all_assets_list = list(df_exposure[code_col].values)

    bounds = [(0, None)] * len(add_assets)
    cons = ({'type': 'eq', 'fun': lambda x: sum(x) - add_weight})
    x0 = np.array([add_weight / len(add_assets)] * len(add_assets))

    add_idx = []
    for i in range(len(all_assets_list)):
        if all_assets_list[i] in add_assets:
            add_idx.append(i)

    arr_exposures = df.drop(columns=[code_col]).to_numpy()
    arr_sigma = df_sigma.to_numpy()

    init_weights = [0] * len(all_assets_list)
    for i in range(len(all_assets_list)):
        if all_assets_list[i] in current_values:
            init_weights[i] = current_values[all_assets_list[i]] / (total_value - add_value)

    fun = lambda x: square_error(exposures=arr_exposures, sigma_f=arr_sigma, init_weights=init_weights,
                                 add_idx=add_idx, add_weights=x)
    res = minimize(fun=fun, x0=x0, constraints=cons, bounds=bounds,
                   options={'maxiter': 50, 'disp': False})
    res_weights = list(res.x)

    res_dict = {}
    for i in range(len(res_weights)):
        res_dict[all_assets_list[add_idx[i]]] = res_weights[i] * add_value / add_weight

    return res_dict


def in_opt_with_init(df_exposure, df_sigma, code_col, current_values, init_distribution, bound_ratio=0.5):
    """

    :param df_exposure:
    :param df_sigma:
    :param code_col:
    :param current_values:
    :param init_distribution: 字典格式，初始设定的加仓分配，key是股票代码，value是金额
    :param bound_ratio:
    :return:
    """
    current_value = sum(current_values.values())
    add_value = sum(init_distribution.values())
    total_value = current_value + add_value
    add_weight = add_value / total_value

    all_assets_set = set([])
    for asset in current_values:
        all_assets_set.add(asset)
    for asset in init_distribution:
        all_assets_set.add(asset)
    df = df_exposure[df_exposure[code_col].isin(all_assets_set)]

    all_assets_list = list(df_exposure[code_col].values)
    x0 = []
    add_idx = []
    for i in range(len(all_assets_list)):
        if all_assets_list[i] in init_distribution:
            x0.append(init_distribution[all_assets_list[i]] * add_weight / add_value)
            add_idx.append(i)
    bounds = []
    for i in range(len(x0)):
        bounds.append((bound_ratio * x0[i], x0[i] / bound_ratio))

    cons = ({'type': 'eq', 'fun': lambda x: sum(x) - add_weight})

    arr_exposures = df.drop(columns=[code_col]).to_numpy()
    arr_sigma = df_sigma.to_numpy()

    init_weights = [0] * len(all_assets_list)
    for i in range(len(all_assets_list)):
        if all_assets_list[i] in current_values:
            init_weights[i] = current_values[all_assets_list[i]] / (total_value - add_value)

    fun = lambda x: square_error(exposures=arr_exposures, sigma_f=arr_sigma, init_weights=init_weights,
                                 add_idx=add_idx, add_weights=x)
    res = minimize(fun=fun, x0=x0, constraints=cons, bounds=bounds,
                   options={'maxiter': 50, 'disp': False})
    res_weights = list(res.x)

    res_dict = {}
    for i in range(len(res_weights)):
        res_dict[all_assets_list[add_idx[i]]] = res_weights[i] * add_value / add_weight

    return res_dict

    pass


def out_optimization(df_exposure, df_sigma, code_col, current_values, minus_assets, minus_value):
    """

    :param df_exposure:
    :param df_sigma:
    :param code_col:
    :param current_values:
    :param minus_assets:
    :param minus_value:
    :return:
    """
    minus_value = abs(minus_value)
    total_value = sum(current_values.values())
    minus_weight = -minus_value / total_value

    df = df_exposure[df_exposure[code_col].isin(current_values)]
    all_assets_list = list(df[code_col].values)

    bounds = []
    cons = ({'type': 'eq', 'fun': lambda x: sum(x) - minus_weight})
    x0 = np.array([minus_weight / len(minus_assets)])
    add_idx = []
    for i in range(len(all_assets_list)):
        if all_assets_list[i] in minus_assets:
            add_idx.append(i)
            bounds.append((-current_values[all_assets_list[i]], 0))

    arr_exposures = df.drop(columns=[code_col]).to_numpy()
    arr_sigma = df_sigma.to_numpy()

    init_weights = [0] * len(all_assets_list)
    for i in range(len(all_assets_list)):
        if all_assets_list[i] in current_values:
            init_weights[i] = current_values[all_assets_list[i]] / total_value

    fun = lambda x: square_error(exposures=arr_exposures, sigma_f=arr_sigma, init_weights=init_weights,
                                 add_idx=add_idx, add_weights=x)
    res = minimize(fun=fun, x0=x0, constraints=cons, bounds=bounds,
                   options={'maxiter': 50, 'disp': False})
    res_weights = list(res.x)

    res_dict = {}
    for i in range(len(res_weights)):
        res_dict[all_assets_list[add_idx[i]]] = res_weights[i] * minus_value / abs(minus_weight)

    return res_dict


def out_opt_with_init(df_exposure, df_sigma, code_col, current_values, init_distribution, bound_ratio=0.5):
    """

    :param df_exposure:
    :param df_sigma:
    :param code_col:
    :param current_values:
    :param init_distribution:
    :param bound_ratio:
    :return:
    """
    for asset in init_distribution:
        init_distribution[asset] = abs(init_distribution[asset])
    total_value = sum(current_values.values())
    minus_value = sum(init_distribution.values())
    minus_weight = -minus_value / total_value

    df = df_exposure[df_exposure[code_col].isin(current_values)]
    all_assets_list = list(df[code_col].values)

    x0 = []
    add_idx = []
    for i in range(len(all_assets_list)):
        if all_assets_list[i] in init_distribution:
            x0.append(init_distribution[all_assets_list[i]] * minus_weight / minus_value)
            add_idx.append(i)
    bounds = []
    for i in range(len(x0)):
        bounds.append((x0[i] / bound_ratio, bound_ratio * x0[i]))

    cons = ({'type': 'eq', 'fun': lambda x: sum(x) - minus_weight})

    arr_exposures = df.drop(columns=[code_col]).to_numpy()
    arr_sigma = df_sigma.to_numpy()

    init_weights = [0] * len(all_assets_list)
    for i in range(len(all_assets_list)):
        if all_assets_list[i] in current_values:
            init_weights[i] = current_values[all_assets_list[i]] / total_value

    fun = lambda x: square_error(exposures=arr_exposures, sigma_f=arr_sigma, init_weights=init_weights,
                                 add_idx=add_idx, add_weights=x)
    res = minimize(fun=fun, x0=x0, constraints=cons, bounds=bounds,
                   options={'maxiter': 50, 'disp': False})
    res_weights = list(res.x)

    res_dict = {}
    for i in range(len(res_weights)):
        res_dict[all_assets_list[add_idx[i]]] = res_weights[i] * minus_value / abs(minus_weight)

    return res_dict
