import os
import json
import logging
import argparse
from glob import glob
from datetime import datetime

import pandas as pd
from sqlalchemy.orm import sessionmaker

from model import Processo, Movimento
from config import connect_db



conn_db = connect_db() #establish connection
Session = sessionmaker(bind=conn_db)
session = Session()

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--segmento', '-sj', type=str, choices=['eleitoral', 'estadual', 'federal', 'militar', 'trabalho', 'tribunal_superior'], help='Escolher qual é o segmento da justica. Ex.: eleitoral, estadual, etc.')
parser.add_argument('--eleitoral', '-tre', type=str, choices=['ac', 'al', 'ap', 'am', 'ba', 'ce', 'df', 'es', 'go', 'ma', 'mt', 'ms', 'mg', 'pa', 'pb', 'pr', 'pe', 'pi', 'rj', 'rn', 'rs', 'ro', 'rr', 'sc', 'sp', 'se', 'to'], help='Escolher qual Estado do segmento da justica eleitoral')
parser.add_argument('--estadual', '-tje', type=str, choices=['ac', 'al', 'ap', 'am', 'ba', 'ce', 'df', 'es', 'go', 'ma', 'mt', 'ms', 'mg', 'pa', 'pb', 'pr', 'pe', 'pi', 'rj', 'rn', 'rs', 'ro', 'rr', 'sc', 'sp', 'se', 'to'], help='Escolher qual Estado do segmento da justica estadual')
parser.add_argument('--federal', '-trf', type=int, choices=list(range(1, 6)), help='Escolher qual número (do 1 ao 5) referente ao segmento da justiça federal.')
parser.add_argument('--militar', '-tjm', type=str, choices=['mg', 'rs', 'sp'], help='Escolher qual Estado do segmento da justiça federal. Tendo apenas 3 opções (mg, rs, sep)')
parser.add_argument('--trabalho', '-trt', type=int, choices=list(range(1, 25)), help='Escolher qual número (do 1 ao 24) referente ao segmento da justiça do trabalho.')
parser.add_argument('--tribunal_superior', '-ts', type=str, choices=['stj', 'stm', 'tst'], help='Escolher o tribunal superior')
parser.add_argument('--salvar', '-s', help='Persiste os dados no banco de dados', default=False, action='store_true')

args = parser.parse_args()

DIR_JUSTICA_ELEITORAL = os.path.join(os.path.abspath('.'), '../base/justica_eleitoral')
DIR_JUSTICA_ESTADUAL = os.path.join(os.path.abspath('.'), '../base/justica_estadual')
DIR_JUSTICA_FEDERAL = os.path.join(os.path.abspath('.'), '../base/justica_federal')
DIR_JUSTICA_MILITAR = os.path.join(os.path.abspath('.'), '../base/justica_militar')
DIR_JUSTICA_TRABALHO = os.path.join(os.path.abspath('.'), '../base/justica_trabalho')
DIR_TRIBUNAIS_SUPERIORES = os.path.join(os.path.abspath('.'), '../base/tribunais_superiores')


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
    

def _read_json(file_path: str, index_file_path: int):
    try:
        with open(file_path[index_file_path]) as f:
            r = json.load(f)
        return r
    except Exception as e:
        logging.error(e)


# Dados Básicos
# millisInsercao = [field['millisInsercao'] for field in _read_json(files_path, 0)]
siglaTribunal = [field['siglaTribunal'] for field in _read_json(files_path, 0)]
grau = [field['grau'] for field in _read_json(files_path, 0)]
numero = [field['dadosBasicos']['numero'] for field in _read_json(files_path, 0)]
# procEl = [field['dadosBasicos']['procEl'] for field in read_json(files_path, 0)] # deu pau
dataAjuizamento = [pd.to_datetime(field['dadosBasicos']['dataAjuizamento']) for field in _read_json(files_path, 0)]
classeProcessual = [field['dadosBasicos']['classeProcessual'] for field in _read_json(files_path, 0)]
# nomeOrgao = [field['dadosBasicos']['orgaoJulgador']['nomeOrgao'] for field in read_json(files_path, 0)] # deu pau
codigoOrgao = [field['dadosBasicos']['orgaoJulgador']['codigoOrgao'] for field in _read_json(files_path, 0)]
codigoMunicipioIBGE = [field['dadosBasicos']['orgaoJulgador']['codigoMunicipioIBGE'] for field in _read_json(files_path, 0)]
instancia = [field['dadosBasicos']['orgaoJulgador']['instancia'] for field in _read_json(files_path, 0)]
codigoLocalidade = [field['dadosBasicos']['codigoLocalidade'] for field in _read_json(files_path, 0)]


# Movimento
mov = pd.json_normalize(data=_read_json(files_path, 0), record_path='movimento', meta=['millisInsercao'])
# millisInsercao_movimento = mov['millisInsercao'].tolist()
codigoNacional = (mov['movimentoNacional.codigoNacional']).fillna(0).astype(int).tolist()
dataHora = pd.to_datetime(mov['dataHora']).tolist()


def save_to_database_ORM(session):
    
    list_mov = []
    list_proc = []
    
    
    for (field2, field3, field4, field5,
        field6, field7, field8, field9, field10) in zip(siglaTribunal, 
                                                        grau, 
                                                        numero, 
                                                        dataAjuizamento, 
                                                        classeProcessual, 
                                                        codigoOrgao, 
                                                        codigoMunicipioIBGE, 
                                                        instancia, 
                                                        codigoLocalidade):
        processo = Processo( 
            siglaTribunal=field2, 
            grau=field3, 
            numero=field4, 
            dataAjuizamento=field5, 
            classeProcessual=field6, 
            codigoOrgao=field7, 
            codigoMunicipioIBGE=field8, 
            instancia=field9, 
            codigoLocalidade=field10
        )
        
        list_proc.append(processo)

    
    for (field2, field3) in zip(codigoNacional, dataHora):
        
        for proc in list_proc:
            movimento = Movimento(
                codigoNacional=field2,
                dataHora=field3,
                processo=proc
            )
            
            # Proximos passos - Não deixar a lista dentro do segundo for, e usar uma clausula if para salvar os dados de movimento certo.
        session.add(movimento)
        
        session.commit()


if args.salvar:
    save_to_database_ORM(session=session)
    
    logging.info('Dados salvos no banco de dados!')
else:
    logging.warning('Salve os dados! Para mais informações consulte --help/-h.')
    logging.info(files_path[0])