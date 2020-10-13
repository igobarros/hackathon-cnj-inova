import os
import json
import logging
import argparse
from glob import glob

import sqlalchemy as db



engine = db.create_engine('postgresql+pg8000://admin:123admin@localhost/mydatabase')

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--segmento', '-sj', type=str, choices=['eleitoral', 'estadual', 'federal', 'militar', 'trabalho', 'tribunal_superior'], help='Escolher qual é o segmento da justica. Ex.: eleitoral, estadual, etc.')
parser.add_argument('--eleitoral', '-tre', type=str, choices=['ac', 'al', 'ap', 'am', 'ba', 'ce', 'df', 'es', 'go', 'ma', 'mt', 'ms', 'mg', 'pa', 'pb', 'pr', 'pe', 'pi', 'rj', 'rn', 'rs', 'ro', 'rr', 'sc', 'sp', 'se', 'to'], help='Escolher qual Estado do segmento da justica eleitoral')
parser.add_argument('--estadual', '-tje', type=str, choices=['ac', 'al', 'ap', 'am', 'ba', 'ce', 'df', 'es', 'go', 'ma', 'mt', 'ms', 'mg', 'pa', 'pb', 'pr', 'pe', 'pi', 'rj', 'rn', 'rs', 'ro', 'rr', 'sc', 'sp', 'se', 'to'], help='Escolher qual Estado do segmento da justica estadual')
parser.add_argument('--federal', '-trf', type=int, choices=list(range(1, 6)), help='Escolher qual número (do 1 ao 5) referente ao segmento da justiça federal.')
parser.add_argument('--militar', '-tjm', type=str, choices=['mg', 'rs', 'sp'], help='Escolher qual Estado do segmento da justiça federal. Tendo apenas 3 opções (mg, rs, sep)')
parser.add_argument('--trabalho', '-trt', type=int, choices=list(range(1, 25)), help='Escolher qual número (do 1 ao 24) referente ao segmento da justiça do trabalho.')
parser.add_argument('--tribunal_superior', '-ts', type=str, choices=['stj', 'stm', 'tst'], help='Escolher o tribunal superior')

args = parser.parse_args()

DIR_JUSTICA_ELEITORAL = os.path.join(os.path.abspath('.'), 'base/justica_eleitoral')
DIR_JUSTICA_ESTADUAL = os.path.join(os.path.abspath('.'), 'base/justica_estadual')
DIR_JUSTICA_FEDERAL = os.path.join(os.path.abspath('.'), 'base/justica_federal')
DIR_JUSTICA_MILITAR = os.path.join(os.path.abspath('.'), 'base/justica_militar')
DIR_JUSTICA_TRABALHO = os.path.join(os.path.abspath('.'), 'base/justica_trabalho')
DIR_TRIBUNAIS_SUPERIORES = os.path.join(os.path.abspath('.'), 'base/tribunais_superiores')


if args.segmento in 'eleitoral':
    files_path = [file for file in glob(os.path.join(DIR_JUSTICA_ELEITORAL, f'processos-tre-{args.eleitoral}', '*.json'))]
if args.segmento in 'estadual':
    files_path = [file for file in glob(os.path.join(DIR_JUSTICA_ESTADUAL, f'processos-tj{args.estadual}', '*.json'))]
if args.segmento in 'federal':
    files_path = [file for file in glob(os.path.join(DIR_JUSTICA_FEDERAL, f'processos-trf{args.federal}', '*.json'))]
if args.segmento in 'militar':
    files_path = [file for file in glob(os.path.join(DIR_JUSTICA_MILITAR, f'processos-tjm{args.militar}', '*.json'))]
if args.segmento in 'trabalho':
    files_path = [file for file in glob(os.path.join(DIR_JUSTICA_TRABALHO, f'processos-trt{args.trabalho}', '*.json'))]
if args.segmento in 'tribunal_superior':
    files_path = [file for file in glob(os.path.join(DIR_TRIBUNAIS_SUPERIORES, f'processos-{args.tribunal_superior}', '*.json'))]
    

def read_json(file_path: str, index_file_path: int):
    try:
        with open(file_path[index_file_path]) as f:
            r = json.load(f)
        return r
    except Exception as e:
        logging.error(e)


# Dados Básicos
millisInsercao = [field['millisInsercao'] for field in read_json(files_path, 0)]
siglaTribunal = [field['siglaTribunal'] for field in read_json(files_path, 0)]
grau = [field['grau'] for field in read_json(files_path, 0)]
numero = [field['dadosBasicos']['numero'] for field in read_json(files_path, 0)]
procEl = [field['dadosBasicos']['procEl'] for field in read_json(files_path, 0)] # deu pau
dataAjuizamento = [field['dadosBasicos']['dataAjuizamento'] for field in read_json(files_path, 0)]
classeProcessual = [field['dadosBasicos']['classeProcessual'] for field in read_json(files_path, 0)]
nomeOrgao = [field['dadosBasicos']['orgaoJulgador']['nomeOrgao'] for field in read_json(files_path, 0)] # deu pau
codigoOrgao = [field['dadosBasicos']['orgaoJulgador']['codigoOrgao'] for field in read_json(files_path, 0)]
CodigoMunicipioIBGE = [field['dadosBasicos']['orgaoJulgador']['codigoMunicipioIBGE'] for field in read_json(files_path, 0)]
Instacia = [field['dadosBasicos']['orgaoJulgador']['instancia'] for field in read_json(files_path, 0)]
codigoLocalidade = [field['dadosBasicos']['codigoLocalidade'] for field in read_json(files_path, 0)]


# Movimento
movimento = [field['movimento'] for field in read_json(files_path, 0)]


print(movimento[:2])

