import unicodedata
import six
import numpy as np
import re
import torch
from torch.nn.utils.rnn import pad_sequence
from torch4keras.snippets import *
import random
from pathlib import Path
from .import_utils import is_safetensors_available

is_py2 = six.PY2

if not is_py2:
    basestring = str


def is_string(s):
    """判断是否是字符串"""
    return isinstance(s, basestring)
    

def truncate_sequences(maxlen, indices, *sequences):
    """截断总长度至不超过maxlen"""
    sequences = [s for s in sequences if s]
    if not isinstance(indices, (list, tuple)):
        indices = [indices] * len(sequences)

    while True:
        lengths = [len(s) for s in sequences]
        if sum(lengths) > maxlen:
            i = np.argmax(lengths)
            sequences[i].pop(indices[i])
        else:
            return sequences


def text_segmentate(text, maxlen, seps='\n', strips=None, truncate=True):
    """将文本按照标点符号划分为若干个短句
       
       :param text: 待划分的句子
       :param maxlen: int, 截断长度
       :param seps: 分隔符
       :param strips: ''.strip()
       :param truncate: True表示标点符号切分后仍然超长时, 按照maxlen硬截断分成若干个短句
       :return: List[str], 划分后的句子列表
    """
    text = text.strip().strip(strips)
    if seps and len(text) > maxlen:
        pieces = text.split(seps[0])
        text, texts = '', []
        for i, p in enumerate(pieces):
            if text and p and len(text) + len(p) > maxlen - 1:
                texts.extend(text_segmentate(text, maxlen, seps[1:], strips, truncate))
                text = ''
            if i + 1 == len(pieces):
                text = text + p
            else:
                text = text + p + seps[0]
        if text:
            texts.extend(text_segmentate(text, maxlen, seps[1:], strips, truncate))
        return texts
    elif truncate and (not seps) and (len(text) > maxlen):
        # 标点符号用完，仍然超长，且设置了truncate=True
        return [text[i*maxlen:(i+1)*maxlen] for i in range(0, int(np.ceil(len(text)/maxlen)))]
    else:
        return [text]


def merge_segmentate(sequences, maxlen, sep=''):
    '''把m个句子合并成不超过maxlen的n个句子, 主要用途是合并碎句子

    :param sequences: List(str), 短句子列表
    :param maxlen: int, 最大长度
    :param sep: str, 合并使用的分隔符, 可以是，。等标点符号
    '''
    sequences_new = []
    text = ''
    for t in sequences:
        if text and len(text + sep + t) <= maxlen:
            text = text + sep + t
        elif text:
            sequences_new.append(text)
            text = t
        elif len(t) < maxlen: # text为空
            text = t
        else:
            sequences_new.append(t)
            text = ''
    if text:
        sequences_new.append(text)
    return sequences_new


def text_augmentation(texts, noise_dict=None, noise_len=0, noise_p=0.0, skip_words=None, strategy='random', allow_dup=True):
    '''简单的EDA策略, 增删改
    
    :param texts: 需要增强的文本/文本list
    :param noise_dict: 噪音数据, 元素为str的list, tuple, set
    :param noise_len: 噪音长度, 优先试用
    :param noise_p: 噪音比例
    :param skip_words: 跳过的短语, string/list
    :param strategy: 修改的策略, 包含增insert, 删delete, 改replace, 随机random
    :param allow_dup: 是否允许同一个位置多次EDA
    '''
    def insert(text, insert_idx, noise_dict):
        text = list(text)
        for i in insert_idx:
            text[i] = text[i] + random.choice(noise_dict)
        return ''.join(text)

    def delete(text, delete_idx):
        text = list(text)
        for i in delete_idx:
            text[i] = ''
        return ''.join(text)

    def replace(text, replace_idx, noise_dict):
        text = list(text)
        for i in replace_idx:
            text[i] = random.choice(noise_dict)
        return ''.join(text)

    def search(pattern, sequence, keep_last=True):
        """从sequence中寻找子串pattern, 返回符合pattern的id集合"""
        n = len(pattern)
        pattern_idx_set = set()
        for i in range(len(sequence)):
            if sequence[i:i + n] == pattern:
                pattern_idx_set = pattern_idx_set.union(set(range(i, i+n))) if keep_last else pattern_idx_set.union(set(range(i, i+n-1)))
        return pattern_idx_set

    if (noise_len==0) and (noise_p==0):
        return texts

    assert strategy in {'insert', 'delete', 'replace', 'random'}, 'EDA strategy only support insert, delete, replace, random'

    if isinstance(texts, str):
        texts = [texts]

    if skip_words is None:
        skip_words = []
    elif isinstance(skip_words, str):
        skip_words = [skip_words]

    for id, text in enumerate(texts):
        sel_len = noise_len if noise_len > 0 else int(len(text)*noise_p) # 噪声长度
        skip_idx = set()  # 不能修改的idx区间
        for item in skip_words:
            # insert时最后一位允许插入
            skip_idx = skip_idx.union(search(item, text, strategy!='insert'))

        sel_idxs = [i for i in range(len(text)) if i not in skip_idx]  # 可供选择的idx区间
        sel_len = sel_len if allow_dup else min(sel_len, len(sel_idxs))  # 无重复抽样需要抽样数小于总样本
        if (sel_len == 0) or (len(sel_idxs) == 0):  # 如果不可采样则跳过
            continue
        sel_idx = np.random.choice(sel_idxs, sel_len, replace=allow_dup)
        if strategy == 'insert':
            texts[id] = insert(text, sel_idx, noise_dict)
        elif strategy == 'delete':
            texts[id] = delete(text, sel_idx)
        elif strategy == 'replace':
            texts[id] = replace(text, sel_idx, noise_dict)
        elif strategy == 'random':
            if random.random() < 0.333:
                skip_idx = set()  # 不能修改的idx区间
                for item in skip_words:
                    # insert时最后一位允许插入
                    skip_idx = skip_idx.union(search(item, text, keep_last=False))
                texts[id] = insert(text, sel_idx, noise_dict)
            elif random.random() < 0.667:
                texts[id] = delete(text, sel_idx)
            else:
                texts[id] = replace(text, sel_idx, noise_dict)
    return texts if len(texts) > 1 else texts[0]


def lowercase_and_normalize(text, never_split=()):
    """转小写，并进行简单的标准化"""
    if is_py2:
        text = unicode(text)
    
    # convert non-special tokens to lowercase
    escaped_special_toks = [re.escape(s_tok) for s_tok in never_split]
    pattern = r"(" + r"|".join(escaped_special_toks) + r")|" + r"(.+?)"
    text = re.sub(pattern, lambda m: m.groups()[0] or m.groups()[1].lower(), text)

    # text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join([ch for ch in text if unicodedata.category(ch) != 'Mn'])
    return text


def sequence_padding(inputs, length=None, value=0, seq_dims=1, mode='post'):
    """将序列padding到同一长度"""
    if isinstance(inputs[0], (np.ndarray, list)):
        if length is None:
            length = np.max([np.shape(x)[:seq_dims] for x in inputs], axis=0)
        elif not hasattr(length, '__getitem__'):
            length = [length]

        slices = [np.s_[:length[i]] for i in range(seq_dims)]
        slices = tuple(slices) if len(slices) > 1 else slices[0]
        pad_width = [(0, 0) for _ in np.shape(inputs[0])]

        outputs = []
        for x in inputs:
            x = x[slices]
            for i in range(seq_dims):
                if mode in {'post', 'right'}:
                    pad_width[i] = (0, length[i] - np.shape(x)[i])
                elif mode in {'pre', 'left'}:
                    pad_width[i] = (length[i] - np.shape(x)[i], 0)
                else:
                    raise ValueError('"mode" argument must be "post/right" or "pre/left".')
            x = np.pad(x, pad_width, 'constant', constant_values=value)
            outputs.append(x)

        return np.array(outputs)
    
    elif isinstance(inputs[0], torch.Tensor):
        assert mode in {'post', 'right'}, '"mode" argument must be "post/right" when element is torch.Tensor'
        if length is not None:
            inputs = [i[:length] for i in inputs]
        return pad_sequence(inputs, padding_value=value, batch_first=True)
    else:
        raise ValueError('"input" argument must be tensor/list/ndarray.')


def parallel_apply_generator(func, iterable, workers, max_queue_size, dummy=False, random_seeds=True):
    """多进程或多线程地将func应用到iterable的每个元素中（直接从bert4keras中移植过来）。
    注意这个apply是异步且无序的，也就是说依次输入a,b,c，但是输出可能是func(c), func(a), func(b)。结果将作为一个
    generator返回，其中每个item是输入的序号以及该输入对应的处理结果。
    
    :param dummy: False是多进程/线性，True则是多线程/线性；
    :param random_seeds: 每个进程的随机种子。
    """
    if dummy:
        from multiprocessing.dummy import Pool, Queue
    else:
        from multiprocessing import Pool, Queue

    in_queue, out_queue, seed_queue = Queue(max_queue_size), Queue(), Queue()
    if random_seeds is True:
        random_seeds = [None] * workers
    elif random_seeds is None or random_seeds is False:
        random_seeds = []
    for seed in random_seeds:
        seed_queue.put(seed)

    def worker_step(in_queue, out_queue):
        """单步函数包装成循环执行"""
        if not seed_queue.empty():
            np.random.seed(seed_queue.get())
        while True:
            i, d = in_queue.get()
            r = func(d)
            out_queue.put((i, r))

    # 启动多进程/线程
    pool = Pool(workers, worker_step, (in_queue, out_queue))

    # 存入数据，取出结果
    in_count, out_count = 0, 0
    for i, d in enumerate(iterable):
        in_count += 1
        while True:
            try:
                in_queue.put((i, d), block=False)
                break
            except six.moves.queue.Full:
                while out_queue.qsize() > max_queue_size:
                    yield out_queue.get()
                    out_count += 1
        if out_queue.qsize() > 0:
            yield out_queue.get()
            out_count += 1

    while out_count != in_count:
        yield out_queue.get()
        out_count += 1

    pool.terminate()


def parallel_apply(func, iterable, workers, max_queue_size, callback=None, dummy=False, random_seeds=True, unordered=True):
    """多进程或多线程地将func应用到iterable的每个元素中（直接从bert4keras中移植过来）。
    注意这个apply是异步且无序的，也就是说依次输入a,b,c，但是输出可能是func(c), func(a), func(b)。

    :param callback: 处理单个输出的回调函数；
    :param dummy: False是多进程/线性，True则是多线程/线性；windows需设置dummy=True
    :param random_seeds: 每个进程的随机种子；
    :param unordered: 若为False，则按照输入顺序返回，仅当callback为None时生效。
    """
    generator = parallel_apply_generator(func, iterable, workers, max_queue_size, dummy, random_seeds)

    if callback is None:
        if unordered:
            return [d for i, d in generator]
        else:
            results = sorted(generator, key=lambda d: d[0])
            return [d for i, d in results]
    else:
        for i, d in generator:
            callback(d)


def get_pool_emb(hidden_state=None, pooled_output=None, attention_mask=None, pool_strategy='cls', custom_layer=None):
    ''' 获取句向量

    :param hidden_state: torch.Tensor/List(torch.Tensor)，last_hidden_state/all_encoded_layers
    :param pooled_output: torch.Tensor, bert的pool_output输出
    :param attention_mask: torch.Tensor
    :param pool_strategy: str, ('cls', 'last-avg', 'mean', 'last-max', 'max', 'first-last-avg', 'custom')
    :param custom_layer: int/List[int]，指定对某几层做average pooling
    '''
    if pool_strategy == 'pooler':
        return pooled_output
    elif pool_strategy == 'cls':
        if isinstance(hidden_state, (list, tuple)):
            hidden_state = hidden_state[-1]
        assert isinstance(hidden_state, torch.Tensor), f'{pool_strategy} strategy request tensor hidden_state'
        return hidden_state[:, 0]
    elif pool_strategy in {'last-avg', 'mean'}:
        if isinstance(hidden_state, (list, tuple)):
            hidden_state = hidden_state[-1]
        assert isinstance(hidden_state, torch.Tensor), f'{pool_strategy} pooling strategy request tensor hidden_state'
        hid = torch.sum(hidden_state * attention_mask[:, :, None], dim=1)
        attention_mask = torch.sum(attention_mask, dim=1)[:, None]
        return hid / attention_mask
    elif pool_strategy in {'last-max', 'max'}:
        if isinstance(hidden_state, (list, tuple)):
            hidden_state = hidden_state[-1]
        assert isinstance(hidden_state, torch.Tensor), f'{pool_strategy} pooling strategy request tensor hidden_state'
        hid = torch.masked_fill(hidden_state, (1-attention_mask[:, :, None]).bool(), torch.finfo(hidden_state.dtype).min)
        return torch.max(hid, dim=1).values
    elif pool_strategy == 'first-last-avg':
        assert isinstance(hidden_state, list), f'{pool_strategy} pooling strategy request list hidden_state'
        hid = torch.sum(hidden_state[1] * attention_mask[:, :, None], dim=1) # 这里不取0
        hid += torch.sum(hidden_state[-1] * attention_mask[:, :, None], dim=1)
        attention_mask = torch.sum(attention_mask, dim=1)[:, None]
        return hid / (2 * attention_mask)
    elif pool_strategy == 'custom':
        # 取指定层
        assert isinstance(hidden_state, list), f'{pool_strategy} pooling strategy request list hidden_state'
        assert isinstance(custom_layer, (int, list, tuple)), f'{pool_strategy} pooling strategy request int/list/tuple custom_layer'
        custom_layer = [custom_layer] if isinstance(custom_layer, int) else custom_layer
        hid = 0
        for i, layer in enumerate(custom_layer, start=1):
            hid += torch.sum(hidden_state[layer] * attention_mask[:, :, None], dim=1)
        attention_mask = torch.sum(attention_mask, dim=1)[:, None]
        return hid / (i * attention_mask)
    else:
        raise ValueError('pool_strategy illegal')


def create_position_ids_start_at_padding(input_ids, padding_idx, past_key_values_length=0, start_padding_idx=True):
    """生成padding_ids, 从padding_idx+1开始。忽略填充符号"""
    # The series of casts and type-conversions here are carefully balanced to both work with ONNX export and XLA.
    mask = input_ids.ne(padding_idx).int()
    incremental_indices = (torch.cumsum(mask, dim=1).type_as(mask) + past_key_values_length) * mask    
    return incremental_indices.long() + (padding_idx if start_padding_idx else 0)


def snapshot_download(
    repo_id: str,
    revision: str = None,
    cache_dir: Union[str, Path, None] = None,
    library_name: str = None,
    library_version: str = None,
    user_agent: Union[Dict, str, None] = None,
) -> str:
    """
    Download pretrained model from https://huggingface.co/
    """
    from huggingface_hub import HfApi, hf_hub_download
    from huggingface_hub.constants import HUGGINGFACE_HUB_CACHE

    if cache_dir is None:
        cache_dir = HUGGINGFACE_HUB_CACHE
    if isinstance(cache_dir, Path):
        cache_dir = str(cache_dir)
    log_info(f'Download {repo_id} to {cache_dir}')

    _api = HfApi()
    model_info = _api.model_info(repo_id=repo_id, revision=revision)

    storage_folder = os.path.join(cache_dir, repo_id.replace("/", "_"))
    for model_file in model_info.siblings:
        filename = os.path.join(*model_file.rfilename.split("/"))
        if filename.endswith(".h5") or filename.endswith(".ot") or filename.endswith(".msgpack"):
            continue
        path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            cache_dir=storage_folder,
            # force_filename=filename,
            library_name=library_name,
            library_version=library_version,
            user_agent=user_agent,
        )
        if os.path.exists(path + ".lock"):
            os.remove(path + ".lock")
    return storage_folder
