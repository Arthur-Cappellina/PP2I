import modules.commande as comm

def test_answer():
    l1 = [("1","2","3","4"),("adda","fefef","fdfd")]
    l2 = [("adda",'dad','654'),('daddd',"456","7894")]
    assert comm.fuse(l1,l2) == [["1","2","3","4","adda","dad","654"],["adda","fefef","fdfd","daddd","456","7894"]]

def test_answer2():
    l1 = [(1,2,3,4,5,6),(7,8,9,10)]
    l2 = [(10,11,12,13,14,15),(16,17,18,19)]
    assert comm.fuse(l1,l2) == [[1,2,3,4,5,6,10,11,12,13,14,15],[7,8,9,10,16,17,18,19]]

def test_answer3():
    l1 = []
    l2 = []
    assert comm.fuse(l1,l2) == []


def test_answer4():
    l1 = [('1','2','30'),('5','4')]
    l2 = [(2,3),(4,5,8,9,8,7)]
    assert comm.fuse(l1,l2) == [['1','2','30',2,3],['5','4',4,5,8,9,8,7]]









