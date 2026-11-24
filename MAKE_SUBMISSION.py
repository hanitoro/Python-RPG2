"""Собирает исходники, проверки и (если найден) журнал в один ZIP."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
root=Path(__file__).resolve().parent
out=root/'SUBMISSION_AURION.zip'
selected=list((root/'tasks').glob('*.py')) + list((root/'checks').glob('stage_*.json')) + list(root.glob('journal_aurion*.txt'))
with ZipFile(out,'w',ZIP_DEFLATED) as z:
    for f in selected:
        z.write(f, f.relative_to(root))
print('\nГотово:',out.name)
print('В архиве:',len(selected),'файлов')
if not any('journal_aurion' in x.name for x in selected):
    print('ВНИМАНИЕ: журнал не найден. Скачай его из игры и перемести сюда из «Загрузок», затем запусти ещё раз.')
print('Отправь этот ZIP преподавателю электронно.')
