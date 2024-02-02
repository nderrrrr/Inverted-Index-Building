import json
import os

from tqdm.auto import tqdm
from opencc import OpenCC

# remove duplicate item
def remove_duplicates(lst: list) -> list:
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


# split text into some chunks
def split_list(text: str, chunk_size: int) -> list:
    result = []

    for i in range(0, len(text), chunk_size//2):
        chunk = text[i:i + chunk_size]
        # print(f'i = {i} which is {text[i]}')
        
        if len(chunk) < chunk_size: # complete the end string
            chunk = text[-chunk_size:]    
           
        result.append(chunk) # chunk長度不足可能會補到2次以上
    
    return remove_duplicates(result)


# extract data from give data path
def extract_data(file_path: str, slice: int):
    converter = OpenCC('s2t')
    preprocess_file = []
    
    with open(file_path, "r",encoding="UTF-8") as f:
        data = f.readlines()
        
        for line in data:
            article = json.loads(line)
            text = article['text']
            text_list = []
            
            if len(text) > 128:
                text_list = split_list(text, slice)
                text_list = [converter.convert(text) for text in text_list]
                article['title'] = converter.convert(article['title'])
                
                # print(article)
                # print(text_list)
                # print(f"length of text {int(article['id'])}: {len(text_list[-1])}")
                # print()
                
                for i in range(len(text_list)):                
                    preprocess_file.append({
                        'id': article['id'],
                        'inner_id': int(i),
                        'contents': text_list[i]
                    })
                                        
    return preprocess_file


# process all files and generate json files
def process_files_in_directory(file_path: str, slice: int):
    # file_path = '/user_data/preprocess/wikidata/data'
    output_path = '/user_data/preprocess/wikijson'
    output_path = output_path + f'_{slice}'
    
    dataset = []
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    with tqdm(total=len(os.listdir(file_path))) as pbar:
        for root, dirs, files in os.walk(file_path, topdown=False):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                dataset.extend(extract_data(file_path=file_path, slice=slice))

                pbar.update(1) # update progress bar
            
    with open(output_path+f'/wiki_process_{slice}.json', 'w', encoding='UTF-8') as output:
        json.dump(dataset, output, indent=4, ensure_ascii=False)
        

if __name__ == '__main__':
    file_path = '/user_data/preprocess/wikidata'
    
    for slice in [256, 512, 1024]:
        print('-'*10 + f'Processing Slice {slice}' + '-'*10)
        process_files_in_directory(file_path=file_path, slice=slice)
        