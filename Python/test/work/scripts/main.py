import pandas as pd


def input_yn(prompt):
    print(prompt)
    while True:
        res = input()
        if res in list("yn"):
            break
        print("Неправильный ввод, попробуйте ещё раз")

    return res


data = pd.read_excel("./data/AUTO21053A.xlsx", "data")


while True:
    while True:
        print("Укажите минимальную и максимальную цену через пробел:")
        try:
            min_price, max_price = map(float, input().replace(",", ".").split())
            break
        except Exception:
            print("Неправильный ввод, попробуйте ещё раз")

    def yn_to_est_net(x):
        return "есть" if x == "y" else "нет"

    need_signal = yn_to_est_net(input_yn("Нужна ли сигнализация? [yn]:"))
    need_music = yn_to_est_net(input_yn("Нужна ли музыкальная система? [yn]:"))

    selector_price = (min_price <= data["price"]) & (data["price"] <= max_price)
    selector_need_signal = data["signal"] == need_signal
    selector_need_music = data["music"] == need_music

    selector = selector_price & selector_need_signal & selector_need_music

    chosen = data.loc[selector, :]

    print(chosen.to_markdown(index=False))

    go_on = input_yn("Продолжить? [yn]:")

    if go_on == "n":
        break
