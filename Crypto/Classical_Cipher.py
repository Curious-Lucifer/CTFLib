from string import ascii_lowercase


def simple_freq_analysis(msg: str):
    """
    - input : `msg (str)`
    - output : `deviation (int)` , more close to 0 `msg` is more likely to be English
    """

    msg = list(msg.lower())
    english_freq = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]
    msg_freq = [100 * msg.count(s) / len(msg) for s in ascii_lowercase]
    return int(sum(((mf - ef) / ef) ** 2 for mf, ef in zip(msg_freq, english_freq)))

