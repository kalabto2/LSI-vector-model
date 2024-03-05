import dataPreparation.docLoader as dl
import dataPreparation.processor as pr
import lsi.preparation as prep
import lsi.conceptMatrix as cm
import lsi.querying as qr
import numpy as np


def main():

    documents, U, S, conceptMatrix, values, terms, titles, texts = dl.load_data()

    #  ------- QUERYING -------

    # myQuery = {"q1": "sandoz usda mani sale soviet union"}  # content of doc. 0
    # queryDict = pr.preprocess_data(myQuery)
    # queryMatrix = pr.query_to_document(queryDict['q1'], terms)
    queryMatrix = pr.query_to_document(texts['SHULTZ VISIT TO MOSCOW POSSIBLE, SAY SOVIETS'], terms)
    # queryMatrix = pr.query_to_document(texts[titles[0]], terms)
    queryMatrix = prep.add_weight_to_query(values, queryMatrix)
    queryConcept = cm.query_to_concept(queryMatrix, S, U)

    simDocs = qr.get_similar_docs(conceptMatrix, queryConcept)


    # Sequence data
    # A = prep.add_term_weights(values)
    # print(A.shape)
    #
    # U2, S2, VT2 = cm.singular_value_decomposition(A, A.shape[1]-150)
    # # S2.resize(S2.count_nonzero(), S2.count_nonzero())
    # # VT2.resize(S2.count_nonzero(), VT2.shape[1])
    # # U2 = np.resize(U2, (U2.shape[0], S2.count_nonzero()))
    # # U2.resize(U2.shape[0], S2.count_nonzero())
    # conceptMatrix2 = cm.get_concept_by_document_matrix(S2, VT2)
    # queryConcept2 = cm.query_to_concept(queryMatrix, S2, U2)
    # simDocs2 = qr.get_similar_docs(conceptMatrix2, queryConcept2)

    print(len(simDocs))
    print(simDocs[0])
    print(titles[simDocs[0][0]])
    print(titles[simDocs[1][0]])
    print(titles[simDocs[2][0]])
    print(titles[simDocs[3][0]])
    print(titles[simDocs[4][0]])
    print(documents[titles[simDocs[0][0]]])

    # Sequence results
    # print(simDocs2[0])
    # print(titles[simDocs2[0][0]])
    # print(titles[simDocs2[1][0]])
    # print(titles[simDocs2[2][0]])
    # print(titles[simDocs2[3][0]])
    # print(titles[simDocs2[4][0]])
    # print(documents[titles[simDocs2[0][0]]])

    # TODO:
    # 1. ziskat query ( z dotazu 'Jak udelat LSI' vytvorit dokument)                    -- OK
    # 2. prevest do prostoru konceptu -> conceptQuery ... fce query_to_concept          -- OK
    # 3. porovnat conceptQuery s matici konceptu pomoci fce cosine_similarity           -- OK
    # 4. vysledek porovnavani setridit, vyfiltrovat pres treshold                       -- musi se jeste udelat treshold
    # 5. Pak nejak dekomponovat ty koncepty zas na dokumenty - pres vzorec dekompozice  -- neni treba ...

    # ==========================================

    # pd.set_option("display.max_rows", None, "display.max_columns", 20)
    # dtm2 = pd.DataFrame(A.toarray(), index=terms, columns=titles)
    # ret = dtm2.sort_index()
    # print(ret['CYPRUS LOWERS COPPER PRICE 1.25 CTS TO 67 CTS'])


if __name__ == '__main__':
    main()
