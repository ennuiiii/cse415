#!/usr/bin/python3
'''MilestoneA.py
This runnable file will provide a representation of
answers to key questions about your project in CSE 415.

'''

# DO NOT EDIT THE BOILERPLATE PART OF THIS FILE HERE:

CATEGORIES=['Baroque Chess Agent','Wicked Problem Formulation and A* Search',\
  'Backgammon Agent that Learns','Hidden Markov Models: Algorithms and Applications']

class Partner():
  def __init__(self, lastname, firstname, uwnetid):
    self.uwnetid=uwnetid
    self.lastname=lastname
    self.firstname=firstname

  def __lt__(self, other):
    return (self.lastname+","+self.firstname).__lt__(other.lastname+","+other.firstname)

  def __str__(self):
    return self.lastname+", "+self.firstname+" ("+self.uwnetid+")"

class Who_and_what():
  def __init__(self, team, option, title, approach, workload_distribution, references):
    self.team=team
    self.option=option
    self.title=title
    self.approach = approach
    self.workload_distribution = workload_distribution
    self.references = references

  def report(self):
    rpt = 80*"#"+"\n"
    rpt += '''The Who and What for This Submission

Project in CSE 415, University of Washington, Autumn, 2019
Milestone A

Team: 
'''
    team_sorted = sorted(self.team)
    # Note that the partner whose name comes first alphabetically
    # must do the turn-in.
    # The other partner(s) should NOT turn anything in.
    rpt += "    "+ str(team_sorted[0])+" (the partner who must turn in all files in Catalyst)\n"
    for p in team_sorted[1:]:
      rpt += "    "+str(p) + " (partner who should NOT turn anything in)\n\n"

    rpt += "Option: "+str(self.option)+"\n\n"
    rpt += "Title: "+self.title + "\n\n"
    rpt += "Approach: "+self.approach + "\n\n"
    rpt += "Workload Distribution: "+self.workload_distribution+"\n\n"
    rpt += "References: \n"
    for i in range(len(self.references)):
      rpt += "  Ref. "+str(i+1)+": "+self.references[i] + "\n"

    rpt += "\n\nThe information here indicates that the following file will need\n"+\
     "to be submitted (in addition to code and possible data files):\n"
    rpt += "    "+\
     {'1':"Baroque_Chess_Agent_Report",'2':"Wicked_Problem_Forulation_Report",\
      '3':"Backgammon_Agent_That_Learns_Report", '4':"Hidden_Markov_Models_Report"}\
        [self.option]+".pdf\n"

    rpt += "\n"+80*"#"+"\n"
    return rpt

# END OF BOILERPLATE.

# Change the following to represent your own information:

leon = Partner("Zhang", "leon", "leonz")
qiubay = Partner("Yu", "Qiubay", "qiubay")
team = [leon, qiubay]

OPTION = '4'
# Legal options are 1, 2, 4, and 4.

title = "Reconstruction of Corrupted Protein Sequences"

approach = '''Approach: We will download data from “https://www.ncbi.nlm.nih.gov/protein/XP_519806.2.” 
Using the data, we will first compute the parameter of the hidden Markov model, which are the transition 
probabilities and the emission probabilities. With these probabilities, we will be able to use forward 
algorithm and Viterbi algorithm to predict the most possible hidden state sequence.'''

workload_distribution = '''We have disscussed about our topic. We will soon find the essential
data set for foward algorithm to train and viterbi algorithm to make reconigtion. Leon will collect
all the data from the protein bank and clean them. I will use the cleaned data to find all 
the transition and emission probabilities. Leon will also be primarly working on the viterbi algorithm, 
and I will be primarly working on the foward algorithm. However, both of us will be learning 
how both algorithm work and help each other along the way.'''

reference1 = '''CS 224S / LINGUIST 285 Spoken Language Processing;
    URL: https://web.stanford.edu/class/cs224s/lectures/224s.17.lec3.pdf (accessed Nov. 18, 2019)'''

reference2 = '''EMBOSS Needle,
    available online at: https://www.ebi.ac.uk/Tools/psa/emboss_needle/'''

our_submission = Who_and_what([qiubay, leon], OPTION, title, approach, workload_distribution, [reference1, reference2])

# You can run this file from the command line by typing:
# python3 who_and_what.py

# Running this file by itself should produce a report that seems correct to you.
if __name__ == '__main__':
  print(our_submission.report())