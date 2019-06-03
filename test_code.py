import NNP_extractor as npe
text = '''
A gnarble left his cozy bed along the ocean floor. He dreamt about a place that he had never seen before! He headed to the surface for a glimpse of sun and sky. A trip so long and perilous, he'd be the first to try!
'''
NNP_list = npe.start(text)
print('::'.join(NNP_list))
