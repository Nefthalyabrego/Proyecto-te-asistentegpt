# Bueno para depurar y ejecutar en MacBooks u otros dispositivos similares
out_dir = 'out-assistmade-char'
# Directorio de salida donde se guardarán los resultados y los checkpoints del modelo entrenado
eval_interval = 250
# Intervalo de evaluación durante el entrenamiento para verificar el rendimiento del modelo
# Es frecuente para evitar el sobreajuste
eval_iters = 200
# Número de iteraciones de evaluación que se realizarán durante el entrenamiento
log_interval = 10
# Intervalo de registro para imprimir información sobre el progreso del entrenamiento
# No se imprimirá información con demasiada frecuencia
always_save_checkpoint = False
# Indica si se deben guardar los checkpoints del modelo incluso si no hay mejora en el rendimiento en la validación
# En este caso, los checkpoints solo se guardarán cuando haya una mejora en el rendimiento en la validación
wandb_log = False
# Indica si se utilizará la integración con Weights & Biases para registrar el entrenamiento
# Puede ser reemplazado mediante la línea de comandos si se desea
wandb_project = 'assistantcibersecurity'
# Nombre del proyecto en Weights & Biases donde se registrarán los resultados del entrenamiento
wandb_run_name = 'mini-gpt'
# Nombre de la ejecución en Weights & Biases para identificar el entrenamiento
dataset = 'assistantcibersecurity'
# Nombre del conjunto de datos que se utilizará para entrenar el modelo
gradient_accumulation_steps = 1
# Número de pasos de acumulación del gradiente antes de realizar una actualización de los parámetros del modelo
batch_size = 64
# Tamaño del lote utilizado durante el entrenamiento
block_size = 256
# Tamaño del contexto de los caracteres anteriores utilizado por el modelo
# El modelo tomará en cuenta hasta los n caracteres anteriores para predecir el siguiente
n_layer = 6
# Número de capas en el modelo GPT
n_head = 6
# Número de cabezas de atención en cada capa del modelo GPT
n_embd = 384
# Dimensión del espacio de embedding utilizado por el modelo GPT
dropout = 0.2
# Probabilidad de dropout utilizada durante el entrenamiento para regularizar el modelo
learning_rate = 1e-3
# Tasa de aprendizaje utilizada para actualizar los parámetros del modelo
# Con redes pequeñas, se puede aumentar un poco la tasa de aprendizaje
max_iters = 5000
# Número máximo de iteraciones de entrenamiento
lr_decay_iters = 5000
# Número de iteraciones después del cual se reducirá la tasa de aprendizaje
# Normalmente se establece igual a max_iters
min_lr = 1e-4
# Tasa de aprendizaje mínima después de aplicar la reducción de lr_decay_iters
beta2 = 0.99
# Valor beta2 utilizado en el algoritmo de optimización Adam para actualizar los parámetros del modelo
# Se aumenta un poco debido al número pequeño de tokens por iteración
warmup_iters = 100

