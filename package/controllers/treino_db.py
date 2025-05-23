from package.models.database import DataBase
from package.models.treino import Treino
from package.models.exercicio import Exercicio
class TreinoDB(DataBase):
    def __init__(self):
        super().__init__("treinos.json")
        data = self._load_json()
        if not data or all(not item for item in data):
            self._database = []
        else:
            self._database = [Treino(**item) for item in data]
    def _get_treino(self, name: str)-> Treino:
        for treino in self._database:
            if treino.name == name:
                return treino
        return None
    def _get_exercicio(self, exercicio_name: str,treino_name: str)-> Exercicio:
        treino = self._get_treino(treino_name)
        if treino:
            for exercicio in treino.exercises:
                if exercicio.name == exercicio_name:
                    return exercicio
        return None

    def _add_treino(self, treino: Treino)-> None:
        self._database.append(treino)
        self.__save()
    def _add_exercicio(self, treino_name: str, exercicio: Exercicio)-> None:
        treino = self._get_treino(treino_name)
        if treino:
            treino.exercises.append(exercicio)
            self.__save()
    def _update_exercise(self, exercicio_name: str, treino_name: str, value: int, attr: str):
        # attr deve ser 'weight' ou 'reps' 
        exercicio = self._get_exercicio(exercicio_name,treino_name)
        if attr == "weight":
            exercicio.weight = value
        if attr == "reps":
            exercicio.reps = value    
        self.__save()
    def _remove_treino(self, name: str)-> None:
        treino = self.get_treino(name)
        if treino:
            self._remove_object(treino)
            self.__save()
    def __save(self):
        dict_treinos = []
        for treino in self._database:
            treino_dict = {"name": treino.name}
            exercicios_list = []
            for exercicio in treino.exercises:
                exercicio_dict = {
                    "name": exercicio.name,
                    "weight": exercicio.weight,
                    "reps": exercicio.reps
                }
                exercicios_list.append(exercicio_dict)
            treino_dict["exercises"] = exercicios_list
            dict_treinos.append(treino_dict)
            
        self._save_to_json(dict_treinos)
 
   
 