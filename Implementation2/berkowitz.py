import threading

#________________________________________
#Final Thread for Main Function
class finalThread (threading.Thread):
    def __init__(self,V1,V2):
        self.V1=V1
        self.V2=V2
        self.retVec=[]
        threading.Thread.__init__(self)
        
    def run(self):
        self.retVec=vecMatrixMult(self.V1,self.V2)

#________________________________________
#Matrix Initialization and Multiplication
def vecMatrixMult (vA, vB):
    #rows in matrix A = length of given A vector
    rows_vA = len(vA)
    #rows in matrix B = length of given B vector
    rows_vB = len(vB)
    #columns in matrix A = length of given B vector
    cols_vA = len(vB)
    #columns in matrix B = length of given B vector - 1
    cols_vB = rows_vB-1
    print ""
    print "vA: ", vA
    print "vB: ", vB
    
    #Initialize Matrices for Multiplication
    A = [[0 for row in range(cols_vA)] for col in range(rows_vA)]
    for i in range(rows_vA):
        for j in range(cols_vA):
            #calculate (row) - (column)
            diffA=i-j
            if diffA<0:
                A[i][j]=0
            else:
                A[i][j]=vA[diffA]
                
    if len(vB)>2:
        B = [[0 for row in range(cols_vA)] for col in range(rows_vA)]
        for i in range(rows_vB):
            for j in range(cols_vB):
                diffB=i-j
                if diffB<0:
                    B[i][j]=0
                else:
                    B[i][j]=vB[diffB]
    else:
        B=[[1],[vB[1]]]
    
    #Failsafe for when matrices are incorrect dimensions
    if cols_vA != rows_vB:
        print "Cannot multiply the two matrices. Incorrect dimensions."
        return

    # Create the result Vector matrix
    # Dimensions would be rows_vA * cols_vB
    C = [[0 for row in range(cols_vB)] for col in range(rows_vA)]
    for i in range(rows_vA):
        for j in range(cols_vB):
            for k in range(cols_vA):
            #Standard Multiplication for initial testing
                #C[i][j] += A[i][k]* B[k][j]
            #AND and XOR modifiers
                C[i][j] += A[i][k] and B[k][j]
                C[i][j]= C[i][j]%2         
    
    D=[]
    for i in range(rows_vA):
        D.append(C[i][0])
    print "D:", D
    return D
        
#________________________________________
# Vector Creation
class createVector(threading.Thread):
    def __init__(self,id,a,R,S,M):
        self.id=id
        self.a=a
        self.R=R
        self.S=S
        self.M=M
        self.result=[]
        threading.Thread.__init__(self)
        
    def run(self):
        self.result.append(1)
        self.result.append(self.a)
        temp3=(matrixmult(self.R, self.S))
        self.result.append(temp3[0][0])
        
        for i in range (1, len(self.M)):
            if i>1:
                temp =mPowI(self.M, i)
            else:
                temp=self.M
            
            temp2 = matrixmult(self.R, temp)
            
            temp3=matrixmult (temp2,self.S)
            self.result.append(temp3[0][0])    
        print "Vector Created: ", self.result
        
#________________________________________
# Power function  
def mPowI(M, i):
    result = M
    for j in range(1, i):
        result = matrixmult(result, M)
        
    return result

#________________________________________
# Initial Matrix Multiplication              
def matrixmult (A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    #Failsafe for when matrices are incorrect dimensions
    if cols_A != rows_B:
        print "Cannot multiply the two matrices. Incorrect dimensions."
        return

    # Create the result matrix
    # Dimensions would be rows_A * cols_B8
    C = [[0 for row in range(cols_B)] for col in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
            #Standard Multiplication for initial testing
                #C[i][j] += A[i][k]* B[k][j]
            #AND and XOR modifiers
                C[i][j] += A[i][k] and B[k][j]
                C[i][j]= C[i][j]%2   
    return C

def subMatricies(A):
    a=A[0][0]
    R=[""]
    R[0]=A[0][1:]
    M=list()
    S=[[0 for col in range(1)] for row in range(len(A)-1)]
    
    for i in range(len(A)):
        if i>0:
            S[i-1][0]= (A[i][0])
            M.append (A[i][1:])  
    
    print "Submatrix #:", i
    print "-----------------"
    print "a: " + str(a) + "\n"
    print "R: " + str(R)+ "\n"
    print "S: " + str(S)+ "\n"
    print "M: " + str(M)+ "\n"
    print "-----------------"
    retArray=list()
    temp = [a,R,S,M]
    
    if len(M)>1:
        retArray= subMatricies(M)
        retArray.append(temp)
    else:
        retArray.append(temp)
    
    return retArray

if __name__== "__main__":
    l = []
    L1 = raw_input("Please enter the input file name with its extension: ")
    with open( L1, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) > 0:
                l.append(map(int, line.split(',')))
    #Temporary hardcoded 4x4 A input for debugging           
    #A=[l[0],l[1],l[2],l[3]]
    
    #A input for NxN
    A = []
    for i in range(len(l)):
        A.append(l[i])
    
    print "\t Input Matrix:"
    print A
    print "-----------------"
    arrayOfSubs = subMatricies(A)
    #----------------------------------------------#
    threads=[]
    for i in range(len(arrayOfSubs)):
        t= createVector(i,arrayOfSubs[i][0],arrayOfSubs[i][1],arrayOfSubs[i][2],arrayOfSubs[i][3])
        threads.append(t)
        t.start()
        t.join()
        
        

    #----------------------------------------------#    
    b=0
    
    #Calculates final b
    for i in range(len(threads)):
        if len(threads[i].M)==1:
            b=threads[i].M[0][0]
    
    sortedResults=[]
    
    for i in reversed (range(len(A)-1)):
        if threads[i].id == i:
            sortedResults.append(threads[i].result)
                
    sortedResults.append([1,b])     
    print ""
    print "Sorted Results with base case: " + "\n", sortedResults
    print "--------------------" + "\n"
    
    #----------------------------------------------#
    while len(sortedResults)>1:
        multiThreads=[]
        i=0
        while i < len(sortedResults):
            try:
                t=finalThread(sortedResults[i],sortedResults[i+1])
                t.start()
            except:
                multiThreads.append(sortedResults[i:])
                
            multiThreads.append(t)
            i=i+2
            t.join()
            
            
        sortedResults=[]
        print "\t For Thread Number: ", len(multiThreads)  
        for i in range(len(multiThreads)):
            #print multiThreads[i].retVec
            sortedResults.append(multiThreads[i].retVec)
        print "\t Sorted Results: ", sortedResults
    #----------------------------------------------#
    
    f = open('Result.txt', 'w')
    
    #Write to output file
    for i in range(len(multiThreads)):
        f.write('%s\n' % sortedResults)
    f.close()
    print "\t Output file saved as Result.txt"
