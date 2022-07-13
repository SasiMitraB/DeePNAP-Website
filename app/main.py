'''Program to take inputs from the user in a web-framework and give an output based on a function'''

from flask import Flask, request, render_template, send_file
from DeePNAP.check_inputs import *
from DeePNAP.make_output import *
from tensorflow.keras import models
import numpy as np
from DeePNAP.data_encoding import *

# Protein: MAVRHERVAVRQERAVRTRQAIVRAAASVFDEYGFEAATVAEILSRASVTKGAMYFHFASKEELARGVLAEQTLHVAVPESGSKAQELVDLTMLVAHGMLHDPILRAGTRLALDQGAVDFSDANPFGEWGDICAQLLAEAQERGEVLPHVNPKKTGDFIVGCFTGLQAVSRVTSDRQDLGHRISVMWNHVLPSIVPASMLTWIETGEERIGKVAAAAEAAEAAEASEAASDE
# Nucleic Acid: GAGGCAAGCGAACCGCTCGGTTTGCTGAA


def create_app(testing: bool = True):
        

    app = Flask('')

    app = Flask(__name__)


    @app.route('/')
    def home():
        return render_template("index.html")

    @app.route('/csv_output')
    def csv_output():
        path = "output.csv"
        return send_file(path, as_attachment = True)
    
    @app.route('/how_to_use')
    def how_to_use():
        return render_template("How to Use.html")
    
    @app.route('/about')
    def about_page():
        return render_template("About.html")


    @app.route("/predict", methods=["POST"])
    def predict():
        # Taking the input values from the program
        prot = str(request.form['Protein Sequence'])
        nacid = str(request.form['Nucleic Acid Sequence'])
        mutations = str(request.form["Mutations"])

        protein_check, prot_verify = check_protein(prot)
        nucleic_acid_check, naverify = check_nacid(nacid)
        if prot_verify and naverify:
            #Loading model from file
            model = models.load_model("app/model.h5")
            #Encoding protein and dna as inputs for model
            prot_str = np.zeros((1, 1000, 20))
            dr_str = np.zeros((1, 75, 5))
            prot_str[0, :, :] = prot_encoding(prot)
            dr_str[0, :, :] = dr_encoding(nacid)
            #Passing the protein and nucleic acid into the model
            output = model.predict({"pinp": prot_str, "drinp": dr_str})[0][0]
            print(mutations)
            # convert log base10 (KD) to KD in Joules per moules
            Kd_Value, Ka_value, G_value = make_output(output, nacid, prot)
            Kd_Value = str(Kd_Value) + " mol/lit"
            Ka_value = str(Ka_value) + " lit/mol"
            G_value = str(G_value) + " Kcal/mol"
            if mutations:
                #Applying the Mutation
                m_prot = mutate_protein(prot, mutations)
                #Encoding the Mutation as an input for the model
                mut_str = np.zeros((1, 1000, 20))
                mut_str[0,:,:] = prot_encoding(m_prot)
                #Passing the Mutation as an input into the model
                mut_kd = model.predict({"pinp": mut_str, "drinp": dr_str})[0][0]
                #Getting required values of the output from Model
                mKd_Value, mKa_value, mG_value, ddg = mutant_output(mut_kd, output, nacid, m_prot, mutations)
                mKd_Value = str(mKd_Value) + " mol/lit"
                mKa_value = str(mKa_value) + " lit/mol"
                mG_value = str(mG_value) + " Kcal/mol"
                ddg = str(ddg) + " Kcal/mol"
            else:
                mKd_Value, mKa_value, mG_value, ddg = "","","",""

        else:
            Kd_Value, Ka_value, G_value = "", "", ""
            mKd_Value, mKa_value, mG_value, ddg = "", "", "", ""

        return render_template("index.html",
                            protein_check=protein_check,
                            nucleic_acid_check=nucleic_acid_check,
                            Kd_Value = Kd_Value,
                            Ka_value = Ka_value,
                            G_value = G_value,
                            mKd_Value = mKd_Value,
                            mKa_value = mKa_value,
                            mG_value = mG_value,
                            ddg = ddg
                            )

    return app 




