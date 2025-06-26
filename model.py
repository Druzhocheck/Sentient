from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import gc

# Конфигурация для экономии памяти
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16
)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

model_name = "SentientAGI/Dobby-Mini-Unhinged-Plus-Llama-3.1-8B"
tokenizer = AutoTokenizer.from_pretrained(model_name)

try:
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        torch_dtype=torch.float16,
        device_map="auto",
        low_cpu_mem_usage=True
    )
except Exception as e:
    print(f"Ошибка загрузки модели: {e}")
    model = None

def clear_memory():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

def generate_response(prompt, max_new_tokens=512, temperature=0.7, top_p=0.85):
    if not model:
        return "Модель не загружена"
    
    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                repetition_penalty=1.2  # Увеличиваем штраф за повторения
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Обрезаем только новый сгенерированный текст
        return response[len(prompt):].split('###')[0].strip()  # Удаляем возможные последующие метки
    except RuntimeError as e:
        if "CUDA out of memory" in str(e):
            clear_memory()
            return "Ошибка: Недостаточно памяти GPU. Попробуйте более короткий запрос."
        return f"Ошибка: {str(e)}"
    finally:
        clear_memory()

def chat():
    history = ""
    max_history_tokens = 512  # Ограничиваем историю в токенах
    
    while True:
        try:
            user_input = input("Вы: ").strip()
            if user_input.lower() in ['quit', 'exit', 'выход']:
                break
            if not user_input:
                continue
                
            # Создаём prompt только с последними релевантными частями истории
            prompt = f"### Текущий диалог:\n{history}\n### Новый запрос: {user_input}\n### Ответ:"
            
            # Кодируем для подсчёта токенов
            encoded_history = tokenizer.encode(history)
            if len(encoded_history) > max_history_tokens:
                # Оставляем только последние релевантные части
                encoded_history = encoded_history[-max_history_tokens:]
                history = tokenizer.decode(encoded_history)
            
            response = generate_response(prompt)
            
            # Обновляем историю только существенной информацией
            #if len(history.split('\n')) > 6:  # Если история слишком длинная
            #    history = '\n'.join(history.split('\n')[-3:])  # Оставляем последние 3 строки
            
            print(f"\nDobby: {response}\n")
            #history += f"Пользователь: {user_input}\nАссистент: {response}\n"
            
        except KeyboardInterrupt:
            print("\nЗавершение сеанса...")
            break
        except Exception as e:
            print(f"\nОшибка: {str(e)}\n")
    
    clear_memory()
    return response