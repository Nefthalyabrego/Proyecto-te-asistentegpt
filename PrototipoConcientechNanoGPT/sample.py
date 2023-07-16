"""
Sample from a trained model
"""
import os
import pickle
from contextlib import nullcontext
import torch
import tiktoken
from model import GPTConfig, GPT
import random;


# -----------------------------------------------------------------------------
init_from = 'resume' # ya sea 'resume' (a partir de un out_dir) o una variante de gpt2 (por ejemplo, 'gpt2-xl')
# Indica si se debe iniciar la generación de texto desde un modelo existente ('resume') o utilizar una variante de GPT-2 pre-entrenada
out_dir = 'out' # ignorado si init_from no es 'resume'
# Directorio de salida donde se guardarán los resultados de la generación de texto
start = "\n" # o "" u otros. También se puede especificar un archivo, por ejemplo: "FILE:prompt.txt"
# Texto de inicio para la generación de texto. Puede ser un string directo o especificar un archivo que contenga el texto de inicio.
num_samples = 1 # número de muestras a generar
# Número de muestras de texto que se generarán
max_new_tokens = 500 # número de tokens generados en cada muestra
# Número máximo de tokens que se generarán en cada muestra de texto
temperature = 1.2 # 1.0 = sin cambios, < 1.0 = menos aleatorio, > 1.0 = más aleatorio en las predicciones
# Parámetro de temperatura que controla la aleatoriedad en la generación de texto.
# Un valor mayor hace que las predicciones sean más aleatorias, mientras que un valor menor hace que sean más deterministas.
top_k = 100 # retiene solo los top_k tokens más probables, los demás tienen una probabilidad de 0
# Número de tokens más probables que se mantendrán durante la generación de texto.
# Los tokens con probabilidad más baja se eliminarán de las opciones posibles.
seed = random.randint(1, 25348973256)
# Semilla utilizada para la generación de números aleatorios. Permite reproducir resultados.
device = 'cpu' # ejemplos: 'cpu', 'cuda', 'cuda:0', 'cuda:1', etc.
# Dispositivo de hardware en el que se ejecutará la generación de texto (CPU o GPU)
dtype = 'float32' # 'float32' o 'bfloat16' o 'float16'
# Tipo de datos utilizado para la generación de texto.
compile = False # utilizar PyTorch 2.0 para compilar el modelo y hacerlo más rápido
# Indica si se debe compilar el modelo utilizando PyTorch 2.0 para acelerar la generación de texto.
exec(open('configurator.py').read()) # overrides desde la línea de comandos o el archivo de configuración
# Se ejecuta un archivo llamado "configurator.py" para aplicar configuraciones adicionales al script.
# Esto permite especificar parámetros adicionales desde la línea de comandos o desde un archivo de configuración.
# -----------------------------------------------------------------------------

torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.backends.cuda.matmul.allow_tf32 = True # allow tf32 on matmul
torch.backends.cudnn.allow_tf32 = True # allow tf32 on cudnn
device_type = 'cuda' if 'cuda' in device else 'cpu' # for later use in torch.autocast
ptdtype = {'float32': torch.float32, 'bfloat16': torch.bfloat16, 'float16': torch.float16}[dtype]
ctx = nullcontext() if device_type == 'cpu' else torch.amp.autocast(device_type=device_type, dtype=ptdtype)

# model
if init_from == 'resume':
    # init from a model saved in a specific directory
    ckpt_path = os.path.join(out_dir, 'ckpt.pt')
    checkpoint = torch.load(ckpt_path, map_location=device)
    gptconf = GPTConfig(**checkpoint['model_args'])
    model = GPT(gptconf)
    state_dict = checkpoint['model']
    unwanted_prefix = '_orig_mod.'
    for k,v in list(state_dict.items()):
        if k.startswith(unwanted_prefix):
            state_dict[k[len(unwanted_prefix):]] = state_dict.pop(k)
    model.load_state_dict(state_dict)
elif init_from.startswith('gpt2'):
    # init from a given GPT-2 model
    model = GPT.from_pretrained(init_from, dict(dropout=0.0))

model.eval()
model.to(device)
if compile:
    model = torch.compile(model) # requires PyTorch 2.0 (optional)

# look for the meta pickle in case it is available in the dataset folder
load_meta = False
if init_from == 'resume' and 'config' in checkpoint and 'dataset' in checkpoint['config']: # older checkpoints might not have these...
    meta_path = os.path.join('data', checkpoint['config']['dataset'], 'meta.pkl')
    load_meta = os.path.exists(meta_path)
if load_meta:
    print(f"Loading meta from {meta_path}...")
    with open(meta_path, 'rb') as f:
        meta = pickle.load(f)
    # TODO want to make this more general to arbitrary encoder/decoder schemes
    stoi, itos = meta['stoi'], meta['itos']
    encode = lambda s: [stoi[c] for c in s]
    decode = lambda l: ''.join([itos[i] for i in l])
else:
    # ok let's assume gpt-2 encodings by default
    print("No meta.pkl found, assuming GPT-2 encodings...")
    enc = tiktoken.get_encoding("gpt2")
    encode = lambda s: enc.encode(s, allowed_special={"<|endoftext|>"})
    decode = lambda l: enc.decode(l)

# encode the beginning of the prompt
if start.startswith('FILE:'):
    with open(start[5:], 'r', encoding='utf-8') as f:
        start = f.read()
start_ids = encode(start)
x = (torch.tensor(start_ids, dtype=torch.long, device=device)[None, ...])

# run generation
with torch.no_grad():
    with ctx:
        for k in range(num_samples):
            y = model.generate(x, max_new_tokens, temperature=temperature, top_k=top_k)
            print(decode(y[0].tolist()))
            print('---------------')
