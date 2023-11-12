# zennolab_test

### Общий подход
применяем zero-shot object detection (**GroundingDino*), из полученных bounding boxes считаем их центры и считаем метрику

### Как запустить
1. *git clone https://github.com/MaxLevinsky/zennolab_test.git*
2. *cd zennolab_test*

### Для запуска на GPU
3. *bash Docker/docker_build.sh*
4. *bash Docker/docker_run.sh*

во время выполения docker_run.sh нужно будет указать директорию со входными данными и директорию для артефактов работы скрипта

скрипт *docker_run.sh* запускается с параметром *--gpus all*, если нужно ограничить кол-во карт, этот параметр нужно исправить.

### Для запуска на CPU
3. *bash Docker/cpu/docker_build.sh*
4. *bash Docker/cpu/docker_run.sh*

во время выполения docker_run.sh нужно будет указать директорию со входными данными и директорию для артефактов работы скрипта


пример входных данных

    - input dir
        - squirrels_head
            - <>.jpg
            - <>.json
        ...

### Сохраняемые аретфакты
в output директории, файл result.csv содержит усредненную метрику и усредненное евклидово расстояние


---
**IMPORTANT**

в случае если возникает следующая оибка

    NameError: name '_C' is not defined

нужно установить переменную окружения CUDA_HOME

    export CUDA_HOME=/path/to/cuda

пример:

для того чтобы узнать где установлен CUDA toolkit нужно в терминале ввести
    
    which nvcc

если вывод будет **/usr/local/cuda/bin/nvcc** то

    export CUDA_HOME=/usr/local/cuda

и повторить описанные выше шаги

---