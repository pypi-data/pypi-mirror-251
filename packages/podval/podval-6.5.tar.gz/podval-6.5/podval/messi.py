from PIL import Image
import requests
# Image.open(requests.get('', stream=True).raw)

#Q1
#1
def dosvkig():
    im = Image.open(requests.get('https://sun9-18.userapi.com/impf/1gVYlZdTz2WQ_9Rx67-1og2Ubif1OrB7sYexTg/7svjbpAqyNI.jpg?size=762x502&quality=96&sign=3d3d9511bc67cf6d78fd32a1c50de511&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-23.userapi.com/impf/FMhSYMy_y8t8ajN8zO_39t7n8zrKnI_WYIvlrQ/3EUSyQHM3Og.jpg?size=778x380&quality=96&sign=f4f4fd219f0dfda4d4f70bfba3c2dc9d&type=album', stream=True).raw)
    return im, im2

#2
def dosvkichi2():
    im = Image.open(requests.get('https://sun9-76.userapi.com/impf/KDpkx0NhCTAia6xj5PIjA-gJlLAv82TSO_8iWQ/e3FQxdpj9Xg.jpg?size=446x622&quality=96&sign=07c48476f77e9bef3b19257e4e4f366f&type=album', stream=True).raw)
    print('''
#a
p_1 = sts.chi2.sf(10.9, df=20)
print(f"P(𝜒^2(20) > 10.9) = {p_1:.6f}")

#б
chi2_1 = sts.chi2.isf(0.93, df=5)
print(f"𝜒^2(0.01, 5) = {chi2_1:.5f}")
    ''')
    return im

#3
def dosvkirs():
    im = Image.open(requests.get('https://sun9-27.userapi.com/impf/UCYW13ti9W786LUsSkm1bL1u8pB88BhnMYk7_w/RXGVGdEir88.jpg?size=576x544&quality=96&sign=3689f4d3d3d5e31ea853cceba7d8ed75&type=album', stream=True).raw)
    print('''
p_1 = 1 - sts.t.sf(-1.7, df=5) - sts.t.cdf(-2.5, df=5)
print(f"P(-2.5 =< 𝑡(5) < -1.17) = {p_1:.7f}")

t_1 = sts.t.isf(0.1, df=7)
print(f"𝑡(0.1, 7) = {t_1:.5f}")
    ''')
    return im

#4
def dosvkirf():
    print('4')
    im = Image.open(requests.get('https://sun9-21.userapi.com/impg/VaII4OMUSETmM-elZbxFYnlcfIgE5blUvCU3bQ/N9imK4kvT5E.jpg?size=814x538&quality=96&sign=35830fe84f562a4ebd69c66f969c54a7&type=album', stream=True).raw)
    print('''p_1 = 1 - sts.f.cdf(3.1, dfn=5, dfd=3) - sts.f.sf(10.7, dfn=5, dfd=3)
print(f"P(3.1 =< 1/F(3,5) < 10.7) = {p_1:.6}")

F_1 = sts.f.isf(0.05, dfn=13, dfd=4)
print(f"𝐹(0.05, 13, 4) = {F_1:.5f}")''')
    return im

#5
def dopti():
    print('5')
    print('''Процентная точка(процентиль) - это значение данных, ниже которого падает определенный 
процент наблюдений в распределении.
Квантиль — это статистическая мера, которая делит набор числовых данных на группы одинакового 
размера, включая квартили (4 части), децили (10 частей), процентили (100 частей) и квинтили (5 частей).
Таким образом, связь между процентными точками и квантилями заключается в том, что процентная точка является 
частным случаем квантиля''')
    im0 = Image.open(requests.get('https://sun9-17.userapi.com/impg/ciZqJh1NPZUGf7VTuCp9CCqt7xBJmEXre8KMJQ/fd3SjU0GGRI.jpg?size=692x101&quality=96&sign=bfd3626181f2e30dcb1b23bf5755d87c&type=album', stream=True).raw)
    im = Image.open(requests.get('https://sun9-1.userapi.com/impg/Jb-0htehjbtK_2n2ny-XrGsu92Vy4lh21Dv3YQ/SIii72JU3mw.jpg?size=534x274&quality=96&sign=ee933f7ab7b2ed9028556ce41ecad097&type=album', stream=True).raw)
    im1 =  Image.open(requests.get('https://sun9-43.userapi.com/impg/z3lMg6w5aHELipWiDSxgmiEEWqZY1nK9iFoN7g/-QaULEMB6pw.jpg?size=788x637&quality=96&sign=63a4ca6c3a9aba5c0574b3edee022a47&type=album', stream=True).raw)

    print('''Z2 = sts.gamma(a=0.5, scale=1/0.5)  # задаем Г распределение с параметрами 0.5, 0.5
Z2.cdf(3.7) - Z2.cdf(0.3)''')
    return im0, im, im1

#6
def sosvik():
    print('6')
    print('''Случайной выборкой из конечной генеральной совокупности называется совокупность случайно отобранных 
объектов из генеральной совокупности. Такая выборка обычно предполагает случайный и независимый отбор элементов.

Выборка может быть повторной, при которой отобранный объект (перед отбором следующего) возвращается в генеральную 
совокупность, и бесповторной, при которой отобранный объект не возвращается в генеральную совокупность.''')
    im =  Image.open(requests.get('https://sun9-78.userapi.com/impg/9498-UqhTRDwMt13JvCe8b0MJyPHmfJFXaEb8A/m-GumceDlPM.jpg?size=848x613&quality=96&sign=e6a247e307bdc867568b72b41c40ddde&type=album', stream=True).raw)
    return im

#7
def sosvir():
    print('7')
    im = Image.open(requests.get('https://sun9-77.userapi.com/impg/9sbaz3cegLN-Cwe7wgxlZHiqb2avbRX7ptpFHA/43rNw3e6PTM.jpg?size=1280x473&quality=96&sign=69f218c4c79b0a95d8ef0c69fbd07a5d&type=album', stream=True).raw)
    return im

#8
def zfdmo():
    print('8')
    im = Image.open(requests.get('https://sun9-5.userapi.com/impg/4JcvY-AySMd4ygXvIqfCmw27qf1rsjE6h7l0Fg/A93GWloJ6s4.jpg?size=907x667&quality=96&sign=caa32251f87f002b6a08d50a6bb7f9c3&type=album', stream=True).raw)
    return im  

#9
def sovfr():
    print('9')
    im = Image.open(requests.get('https://sun9-36.userapi.com/impg/wfQ7vCPjUKfTcCMjcZG-9oUAEEdMnTUlGXEexg/I08zTNWWSp4.jpg?size=1280x353&quality=96&sign=972132c6298666bc16bc19953d0425cf&type=album', stream=True).raw)
    im1 = Image.open(requests.get('https://sun9-16.userapi.com/impg/JFadi1Dhn-eiB5I9p8BmTdEHO0nM3RnibNL9aQ/fuIBvBCmDkc.jpg?size=845x588&quality=96&sign=65052ab1f01d01fa3815998623627ab2&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun2-21.userapi.com/impg/QfCnywImf1S4XwqZVXI4LGhv4KRa-LLLnnqQiA/1e12jeuCOKg.jpg?size=1280x537&quality=96&sign=53801b29aa0d7ab500141152e3e389c4&type=album', stream=True).raw)
    return im, im1, im2
    
#10
def dokps():
    print('10')
    im = Image.open(requests.get('https://sun9-66.userapi.com/impg/rsXSza4wthG_fBe8B3GacMweNHREwRDTh_YyFg/oGlrKUPCbtw.jpg?size=1198x580&quality=96&sign=d24296e4259e7ce095dc9675313c33b3&type=album', stream=True).raw)
    im1 = Image.open(requests.get('https://sun9-21.userapi.com/impg/pLElElzeVsp0rG_IDg35AhOCwo7-pMna5IICjQ/bKDV-w8IGlw.jpg?size=1270x382&quality=96&sign=774c1d71d32e54a19fdc6ad1e5273893&type=album', stream=True).raw)
    return im, im1
    
#11
def chttso():
    print('11')
    im = Image.open(requests.get('https://sun9-33.userapi.com/impg/7ltidI6txzxDAg5wTIGjLmxMj8IILxOwJEv-kQ/e_bYENPfjC4.jpg?size=898x551&quality=96&sign=8280b1c0244698e63d6d0394e5b4dffe&type=album', stream=True).raw) 
    im1 = Image.open(requests.get('https://sun9-2.userapi.com/impg/VocezrVqv6Qwult1eTUoTxXOcoPJCj8hLmNSmg/DuuFhabatuM.jpg?size=1280x111&quality=96&sign=6771db647cd35e176c56ad091ebda43d&type=album', stream=True).raw)
    return im, im1

#12
def siddu():
    print('12')
    im = Image.open(requests.get('https://sun9-29.userapi.com/impg/F4TNiKWvNYFIY0Ua30WIzf1NHVyzIBG9Tiw2pQ/Bmc1xjLJx-4.jpg?size=1280x446&quality=96&sign=a08999d6838069bc8819dbdc31e09bd5&type=album', stream=True).raw)
    return im

#13
def sosoo():
    print('13')
    im = Image.open(requests.get('https://sun9-79.userapi.com/impg/ciWDmzrJ-kg-TEEbfZkXzZTBvBTdvv73VDiJaQ/ySP6tjyPcq4.jpg?size=836x197&quality=96&sign=c453b70f30e2ff73ac93eb58e27d0070&type=album', stream=True).raw)
    im1 = Image.open(requests.get('https://sun9-8.userapi.com/impg/FZCA2Xv7kQEDs4asvcMZzrWzl9rHsep0ykxBgA/F8qfy8ik-CY.jpg?size=823x606&quality=96&sign=1d0c50d6be5baa9eb21f86354d45c0b8&type=album', stream=True).raw)
    return im, im1

#14
def skooo():
    print('14')
    im = Image.open(requests.get('https://sun9-57.userapi.com/impg/3p2Wmq-YD-YqfEjkSWW2A4_uZwqZa8euxnZCag/OYE2K_mQ5F4.jpg?size=811x504&quality=96&sign=96bb89a456db58e81e19bf138ed4c5e1&type=album', stream=True).raw)
    return im
    
#15
def doipfi():
    print('15')
    im = Image.open(requests.get('https://sun9-50.userapi.com/impg/jtZXi1sFElgPw80jy94b90Y7zloV9pKHTvd7WA/ppXapV4otZw.jpg?size=813x490&quality=96&sign=2257348b9f6c66c6c9aef9c3177ece58&type=album', stream=True).raw)
    return im

#16
def soeoprkn():
    print('16')
    im = Image.open(requests.get('https://sun9-14.userapi.com/impg/8Wsuvp9wezGTrI48xaF1Szdefrv2mIS8buPDiA/UVhk6o_PL5g.jpg?size=814x617&quality=96&sign=39fb32820c6e6bb485b082f476b37200&type=album', stream=True).raw)
    im1 = Image.open(requests.get('https://sun9-63.userapi.com/impg/tyBz_HT3v1UrhzKtAaezyxd7qRwNBa4sg0Rqtw/oEvc50lWZ8k.jpg?size=817x399&quality=96&sign=c25f1f529c7dedc0cb97d8da17ad32e5&type=album', stream=True).raw)
    return im, im1
    
#17
def dnsie():
    print('17')
    im = Image.open(requests.get('https://sun9-62.userapi.com/impg/7AgF-CEOl0Oznt28R3-uU8E3Hg3waNkE_uZZOw/RHElJVeI_cs.jpg?size=817x413&quality=96&sign=f68d2ac53f3692b65795e78f4d0f9ba3&type=album', stream=True).raw)
    im1 = Image.open(requests.get('https://sun2-18.userapi.com/impg/Yok779UEyhqCU-AtTK8vNlcB0FvNsVBBb0biyg/SeR9-2q4knc.jpg?size=805x508&quality=96&sign=277e527dc401ef29ff1ade32787f5adc&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-75.userapi.com/impg/-NtMNfNVFmQ7tFPemvAkOqdyFFGx3kJdvMTiPg/FTBVRU3Qv7I.jpg?size=804x516&quality=96&sign=9f6834d56d4228ba052489d469f45f86&type=album', stream=True).raw)
    return im, im1, im2

#18
def soeoprkd():
    print('18')
    im = Image.open(requests.get('https://sun9-45.userapi.com/impg/ubH79aMj7CNxjHjz4yLiHILv8jXSHrJ88m44fg/DZjyV5Poa_4.jpg?size=808x271&quality=96&sign=bc755f6014fc022214043312a18e5e56&type=album', stream=True).raw)
    im1 = Image.open(requests.get('https://sun9-64.userapi.com/impg/H9Wv6_O8eEl8rwADrO1IeNyCa6z1QzZrWr14uA/mpe2vBGHY8c.jpg?size=1042x580&quality=96&sign=ce50e0ed456cec0a7e6668a6a67a13b5&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-74.userapi.com/impg/umE8XMwWzKlV6CVF88WFFfGRrdwzbzXdhrQ3wg/QihC_VKHJ1s.jpg?size=909x646&quality=96&sign=b7ef07756129c4a469acf2d3c079824a&type=album', stream=True).raw)
    return im, im1, im2
    
#19
def sinrk():
    print('19')
    im = Image.open(requests.get('https://sun9-20.userapi.com/impg/RCxibiMqP3Ndeg3ygsQTClXCuChm5K6NX6qYyw/_1fFvng0s6s.jpg?size=986x650&quality=96&sign=42cb50150fdcc6ae435198dd3289607f&type=album', stream=True).raw)
    im1 = Image.open(requests.get('https://sun9-66.userapi.com/impg/dO_DSPJraa_5xYeUqUdOi0KtIMlWduOlEwGIYA/YwlQCgpOzt4.jpg?size=977x615&quality=96&sign=73ca5ff247b2fb166a4cea552145d910&type=album', stream=True).raw)
    return im, im1

#20
def doipfv():
    print('20')
    im = Image.open(requests.get('https://sun9-52.userapi.com/impg/aomHQJLEiy3vZhh33fc6osRH-bhxPdOJH3K7jw/MEzTbuBfHUc.jpg?size=892x274&quality=96&sign=0ae63824dd465474fc5fb117b7f8a13f&type=album', stream=True).raw)
    im1 = Image.open(requests.get('https://sun9-68.userapi.com/impg/tZghTzyY46egFqLRyfk2GKvV9Aw01OIm65_O4w/Qe1Y1szdeCI.jpg?size=1261x584&quality=96&sign=ef36e095390a06d94ab584e910fb05a4&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-23.userapi.com/impg/IhStPJfivGRz7Pq_chriILo9yDSTIjbEOQdQdg/oGZ4mnPGG0c.jpg?size=1087x637&quality=96&sign=23790288f73ee45a0cba787b570fc89f&type=album', stream=True).raw)
    return im, im1, im2
    
#21
def kpopa():
    print('21')
    im = Image.open(requests.get('https://sun9-74.userapi.com/impg/HOYfJJ8_6xBkZkCez_dV8-1yrckQNu9ObWqiaQ/m6sy0yaBAYU.jpg?size=762x690&quality=96&sign=5ca3c01c24f67eaab943feebcd042d06&type=album', stream=True).raw)
    im1 = Image.open(requests.get('https://sun9-3.userapi.com/impg/XxJ50Mt0T-aAw8362Nz660RA1mU_7pVvF_PbbQ/Jgazbpr1D_w.jpg?size=695x678&quality=96&sign=f71209ad4e5a274d3860bddb053c98fc&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-76.userapi.com/impg/hw05VSPKVnpj-vhyklbL7R2gKr9EBWg1EdDeqQ/CWzyiNFcLKI.jpg?size=611x288&quality=96&sign=82f9b2fdf9be9b1e14d31d341594a4dc&type=album', stream=True).raw)
    return im, im1, im2

#22
def kpopr():
    print('22')
    im = Image.open(requests.get('https://sun9-26.userapi.com/impg/mM3cMoQNRMubjkQstOO9e8rbbpum5z173xuwCw/ps0PaBVPTKs.jpg?size=647x455&quality=96&sign=6cc5d70685fb1992a742a7f8bccbd4f2&type=album', stream=True).raw)
    im1 = Image.open(requests.get('https://sun9-74.userapi.com/impg/CTy7fKEf2MNP23sOrWSHiIkbiG2I3LRE2_WocQ/wByPb6-VrV4.jpg?size=1178x325&quality=96&sign=6b7cebb43480c76e5d7172e2ca57d1a2&type=album', stream=True).raw)
    return im, im1

#23
def sodop():
    print('23')
    im = Image.open(requests.get('https://sun9-11.userapi.com/impg/bKBEDj6FCP2cYrGNps5iLPHQ6zGaUoCuM-YjDw/6y4LEOm0c7Q.jpg?size=811x567&quality=96&sign=2bce81972141f2c87b2e73eb9f4d53e8&type=album', stream=True).raw)
    im1 = Image.open(requests.get('https://sun9-17.userapi.com/impg/FmMPIZOj4If9w-DkstR0gN-3lLVe6QvetIHxxw/9x7eGocc_ZE.jpg?size=1015x333&quality=96&sign=9d5a9e98af8269ff94f7decda5a66ac4&type=album', stream=True).raw)
    return im, im1

#24
def pfsvd_var_i():
    im = Image.open(requests.get('https://sun9-63.userapi.com/impg/8lGArErKKG2QIBwnVYm-eCqnByO-rpsXvJZFjg/fV0kTXCi0fA.jpg?size=728x461&quality=96&sign=06959d2b4272a2900afef3468f38bd67&type=album', stream=True).raw)
    return im

#25
def pfsvd_mu_i():
    im = Image.open(requests.get('https://sun9-25.userapi.com/impg/y2KP4iWmp8ksqHutP1Zu_Lcr9NnfRbLkxgZBVQ/0LT1mvY9dpI.jpg?size=720x674&quality=96&sign=83ead7169dc049c03480ccb75331188b&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-63.userapi.com/impg/OMivNN7xTPspo7PPrOWjpXMU9BJChpXkjZsMUg/PLcZtV7CXkw.jpg?size=726x480&quality=96&sign=328ea48c0abd4a74f5199beb53b466ec&type=album', stream=True).raw)
    return im, im2

#26
def pfsvd_var_n():
    im = Image.open(requests.get('https://sun9-6.userapi.com/impg/pl03oJHSuUAaKdfDHznOJT9b-Mq9NNgQoZR9BA/GjcSs4oPFtw.jpg?size=1004x483&quality=96&sign=29368205c89bfa43be3f770027c7a53a&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-76.userapi.com/impg/0d4KbN-eYzA1mOrJkcBV0qBl_EgQbERKwY4S3A/5iH_edd3jlM.jpg?size=734x689&quality=96&sign=4ed79ca031847e0c06fefe2078fca9ee&type=album', stream=True).raw)
    return im, im2

#27
def pfsvd_mu_n():  
    im = Image.open(requests.get('https://sun9-23.userapi.com/impg/IcufMvFxOHTA9ngkhZ8ohhf0ASUgqSz7XqjV6w/iqLiqYwdcTo.jpg?size=1025x634&quality=96&sign=a456f43605bdf210076d1533db6a7613&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-67.userapi.com/impg/Lw9f-WqI79RhE9-aB7ykfftZ6Np7MBnftSbkSw/R5BUbYDM6eg.jpg?size=749x530&quality=96&sign=8efff6fbce599852ace148d8f8d9ac02&type=album', stream=True).raw)
    return im, im2

#28
def stfpv():
    im = Image.open(requests.get('https://sun9-37.userapi.com/impg/OjfRv_OtfGbz1grMOyUbsgFAZ1fzGL6loS4Bpg/Cunl-ljzMTw.jpg?size=881x272&quality=96&sign=618abde61928ef595deb126230fd52aa&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-62.userapi.com/impg/uWyHtLoFmgNLltXMSavZbd6lk8anVcCFj8ocaA/yYa1zakMMPY.jpg?size=725x599&quality=96&sign=3f019d46bda3d94f46f17280cc4ae3ad&type=album', stream=True).raw)
    return im, im2

#29
def pfsvd_pred():
    im = Image.open(requests.get('https://sun9-27.userapi.com/impg/ZQcQ6XML7ZOYMW-8yvplRu5xbVSC--raED_adQ/PWI6RyLXY3Q.jpg?size=673x757&quality=96&sign=830ab40e38b9b049c9e637826c4325ee&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-49.userapi.com/impg/t-Flys_nO5KNEPZI0pSbPk3IWOOHTa-gaipHNA/VilnI_LT4D4.jpg?size=678x748&quality=96&sign=0f1af1eae3974640483e728a24316aed&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-20.userapi.com/impg/lHo_ltTE8l8SlWgDrEExDQk9AuoxhREenoulEg/UWRMkq4oOoU.jpg?size=763x528&quality=96&sign=418bf593877b901e60e9a63e4fdfc7a8&type=album', stream=True).raw)
    return im, im2, im3

#30
def doadi_rho():
    im = Image.open(requests.get('https://sun9-36.userapi.com/impg/tVDN1FHnbeOgFQVI69XhT72-Y3ipmUxSIiwVMg/mRGIBRwhZ8U.jpg?size=736x529&quality=96&sign=39f0ffca14b9e159974bd05a4d5d62a5&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-67.userapi.com/impg/u0seTHggGdc0DtVq0CJTbecmmoMbWBMkLrUVCg/SGXPfOIqH_E.jpg?size=699x765&quality=96&sign=4f538d00b72ee87028cef82aa7e28403&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-24.userapi.com/impg/zrvtNsr4JrPx8oevGM8xHUEkduxR-MrmW0PpLg/XFa4agdSdo0.jpg?size=770x729&quality=96&sign=42c86de3220649debb3aed87a11aeec2&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-18.userapi.com/impg/ufZeWvNDYiaMD8CepuaKIGw6H1geD_f9BMbKpQ/Han7htxDjls.jpg?size=627x779&quality=96&sign=4a07aa8b488cb4d308b0fabd20068999&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-57.userapi.com/impg/Eq9cQRAoshQ98C1r527euwaShxx_m30MFwFT2Q/CTmpxpvKDJE.jpg?size=680x417&quality=96&sign=1901aba4420049c65dd68a4de6b5318f&type=album', stream=True).raw)
    return im, im2, im3, im4, im5

#31
def doadi_prob():
    im = Image.open(requests.get('https://sun9-65.userapi.com/impg/Lcm8oF4QKJojmG_dMOGJw8EGSlTEuKfxHo5zKQ/O0rF-R9IeAk.jpg?size=752x594&quality=96&sign=ef21b661a20297ce043e8eae130d79ef&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-25.userapi.com/impg/tkm8hfAHp04_ZtPwlyFFeEK25bLnguQE8q79Xg/Yv6ljffcRFs.jpg?size=672x424&quality=96&sign=796cb24e34fd10d728e1351d65d7f03a&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-80.userapi.com/impg/VWT9dZ9db1y3xYiv8hkCDayGVGU2zUlZ4gorqw/vCGVruQtXYo.jpg?size=684x754&quality=96&sign=b7cbec1f3cdb907c6813837139a8eb73&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-67.userapi.com/impg/IbAYWim210RRgTTYpO-nVZwVrQ8CnG1h2_sUgg/0LPRbOXRP1E.jpg?size=678x542&quality=96&sign=d2ae62d1c243253f0fb7a87cf6d4987e&type=album', stream=True).raw)
    return im, im2, im3, im4

#32
def pvoig_ost_var():
    im = Image.open(requests.get('https://sun9-66.userapi.com/impg/OLHssBF6ZHRfYtkz4kn_BZdMTChMhRVL5GkUfQ/TNi16ty84wk.jpg?size=761x969&quality=96&sign=2bc20765f301ac63d6d5817e50631bfb&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-78.userapi.com/impg/9RqOeKhIgI6kLhoSn0XH5zx195n1qGtnGInu4Q/7qyImgJ5cdA.jpg?size=766x293&quality=96&sign=07c0aaff73f9deea2f05dfe1b96447b3&type=album', stream=True).raw)
    return im, im2

#33
def pvoig_var_tozhd():
    im1 = Image.open(requests.get('https://sun9-61.userapi.com/impg/rbZZHKZjaLNGdUdyJRnK_EEmX19ueRjC1AB3ug/Gj_MFaEVv9c.jpg?size=944x1256&quality=96&sign=1eb9f94dc1516d8f6dc2c965508644b6&type=album', stream=True).raw)
    return im1

#34
def pvoig_fact_var():
    im1 = Image.open(requests.get('https://sun9-37.userapi.com/impg/okDLyDz0OEXrjvzgZBmDgfbXrdeYEkf0-bQ47A/IzD9YnkNTfU.jpg?size=527x292&quality=96&sign=d233c07bb6d561c4faf98c8de3d0323d&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-8.userapi.com/impg/9TGCkW0z0w49SVCHg5gtXQcRfTTJNTEtujFgsA/YJTlpAHK4Yw.jpg?size=499x810&quality=96&sign=4dc1b1e260130dd8f987f170b0d65a29&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-14.userapi.com/impg/_WigUC8mb12KR2qH2bjgwDYH1wPChLSOajaWRA/Znm5XegK49g.jpg?size=488x640&quality=96&sign=6e5f818fa0deff060298f7704445ee27&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-67.userapi.com/impg/TXvbHtP8NEIuVu3xTdnum_gctuDxr-yzuHmQ8w/kV--L8B1WzA.jpg?size=506x137&quality=96&sign=6f2233585cc9d3dc668047bca51f23d2&type=album', stream=True).raw)
    return im1, im2, im3, im4


#Q2
#1
def oosps():
    im = Image.open(requests.get('https://sun9-70.userapi.com/impg/rYPRjV-448jFsUmA6yKintvc5Dnr15kzPE9FBg/7pItPCuxWnQ.jpg?size=730x730&quality=96&sign=c0140fecd504b01097a5e5a1554f82d8&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-13.userapi.com/impg/GEWiidi-1TuifupDHxJncs6kFX9O8lzf6hjrWQ/8on163zObCQ.jpg?size=741x384&quality=96&sign=dd48ec26519573f75c2b203cc6d9d6b4&type=album', stream=True).raw)
    return im, im2

#2
def pviop():
    im = Image.open(requests.get('https://sun9-10.userapi.com/impg/b5Iq7CreWzV0G29kROpkM6TIzGrHORh4KKTTdg/X4ACasMnhuY.jpg?size=745x567&quality=96&sign=5d425fd74bff74fb6a700fdb8618c75c&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-42.userapi.com/impg/BOFSksL5IyFX2E8f3nqQHO1ExcMY3cPFWfjqtg/2NMtr-Q31mQ.jpg?size=685x736&quality=96&sign=764852e831001f6281cdc39a2bbd6f95&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-66.userapi.com/impg/PDH-03fkNjcxfsOso190qZCqXFZygtjPn8Y5yQ/iw2yPUimB4o.jpg?size=679x710&quality=96&sign=b8b1c49e8ddc3d056338ad8063e2bfe3&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-57.userapi.com/impg/YyaUjZRfcJ0Hcek1c46nm5zeGfNTXeJUEE_Vpg/cjq_ikLs1KU.jpg?size=683x715&quality=96&sign=449425a0c9ab9182d05f8c9fd16dfbe3&type=album', stream=True).raw)
    return im, im2, im3, im4

#3
def donis():
    im = Image.open(requests.get('https://sun9-68.userapi.com/impg/aaZ_35kLslBGTihVbL2prumCu5a8ytnthy9DxQ/opIyE132Gd4.jpg?size=764x522&quality=96&sign=9130feba0e3a9eba9f90eb5843f28851&type=album', stream=True).raw)
    return im

#4
def slnpv():
    im = Image.open(requests.get('https://sun9-32.userapi.com/impg/0l9Xf_-7GdzmkyFWWOimNzKirWOx1uhGgy0jrQ/0WwIdq_l7Tc.jpg?size=741x620&quality=96&sign=eacbc5e54758fadeee07282be1a42650&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-34.userapi.com/impg/KYo722qQ8gQS3Szpq4o72oNmwhn8zWVR0XMNHQ/TtJfmKiKO7A.jpg?size=688x437&quality=96&sign=5071ecbb9d2f8c8649a392845a85da30&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-13.userapi.com/impg/ASKw9K1mShUg4TMpRzcusR-IYkiPPVIscupRbw/a5wseUBE2ik.jpg?size=685x411&quality=96&sign=1e9870689c85f46b5fa038ed9c24cf6c&type=album', stream=True).raw)
    return im, im2, im3

#5
def pvoin_var_izv_mu_b():
    im1 = Image.open(requests.get('https://sun9-5.userapi.com/impg/XqxMzJilhjkTapC9sVSOK0lhIcWO4UTztpV3pA/gVwwlviTOyE.jpg?size=865x604&quality=96&sign=e8fcea3a97f72bc2b0ef36dcae80f04f&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-59.userapi.com/impg/pEASMcJOwDW0hs-FphBuScqndqQEzQ3yhzC9eg/pRWp8kqIQQU.jpg?size=901x264&quality=96&sign=12889d8d419f572c125160c4fb772970&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-73.userapi.com/impg/QVaWIIu2pY70b8weUod4DMnE7zj4xQ7Pvs5X-Q/2aXXWBhU81Q.jpg?size=1228x397&quality=96&sign=7bcac7331ce189482f78d0ab82ae1d44&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-57.userapi.com/impg/PUT7V9jI1zUyNtEJr-keC1cV57vAcSxnHth-cw/fOCJLxz8Pgo.jpg?size=911x294&quality=96&sign=e21218a03c00ae52e6785110acaca8ef&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-15.userapi.com/impg/FATzigM5Uz1yDBWMpdkJ3fx0VCX5oT_f4x_epg/GzxO5gp3lLg.jpg?size=1260x503&quality=96&sign=f35d9efca542efbf770c3ad89d7773c5&type=album', stream=True).raw)
    im6 = Image.open(requests.get('https://sun9-50.userapi.com/impg/CwnNM_2enKTka0CYM66Yqg0cSXmGn-gJpkatLQ/qp0LIDjsvzc.jpg?size=897x517&quality=96&sign=78a6e2720e2ad9b1e2076be4bce12930&type=album', stream=True).raw)
    im7 = Image.open(requests.get('https://sun9-27.userapi.com/impg/sKVJtTkQbdxoo-_OFLqt391LMPwYJhVBS-kAGg/9H0zy19m8M8.jpg?size=602x480&quality=96&sign=089bfc32aaf528fa035376645950de49&type=album', stream=True).raw)
    return im1, im2, im3, im4, im5, im6, im7

#6
def pvoin_var_izv_mu_m():
    im1 = Image.open(requests.get('https://sun9-20.userapi.com/impg/c01ISdJrMfcVVGkNwqVBuSf_YSCSxR1gXorS-w/2neHZ0uzSKE.jpg?size=809x555&quality=96&sign=8566ce0d45df81d716f21526496b31e8&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-4.userapi.com/impg/xJEDIgnoc3LKKsEdbwgsO9a7GEWrap31RvsXAA/h_K2a7ci_Os.jpg?size=822x236&quality=96&sign=d401ccda0e147ceecc6fc86dc568d812&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-78.userapi.com/impg/vamWaCTd7Jgk-pRxAQC_671C2CikLbQKTYTxtQ/Jh9u-vycbKE.jpg?size=1106x360&quality=96&sign=a803b170bcc0acaf5b88b9ac65cec293&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-67.userapi.com/impg/e2qG0JdNFbvPasEIiK3QQqj3ZW4T9NfHtD0EzQ/ViVTquPISEk.jpg?size=806x267&quality=96&sign=7b2a58ea0175eba93091c8483a2a7714&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-25.userapi.com/impg/kOn9_52Uxa7cnIeXg70Qf9loy4D013aC5gR_0A/ATEjjZFHfQs.jpg?size=899x558&quality=96&sign=caaab975081e40cb23b42dab4e217e33&type=album', stream=True).raw)
    return im1, im2, im3, im4, im5

#7
def pvoin_var_izv_mu_n():
    im1 = Image.open(requests.get('https://sun9-42.userapi.com/impg/hWNB740R7vYh2-VV9IAQiZJBGfzi_cRzdw8NmQ/o0aZ4GH_Li0.jpg?size=807x552&quality=96&sign=31d085a8662f2a326c73a9f2be18c34e&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-33.userapi.com/impg/s-ddN4nWHlzS3Gt2BOOEbXVT17TkIhmLKQB3nA/8XPoC1ICpLs.jpg?size=814x230&quality=96&sign=69b59bafafe6afcf66d042386d43a91a&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-44.userapi.com/impg/sgXZ_SwJgYA_-5izygVOBJ90AplcKV_Ha9vBUw/P2bNGqMW7hM.jpg?size=1120x231&quality=96&sign=2f38056df32b207d7dd44bd70843d54b&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-38.userapi.com/impg/6GfzBBiWaxOfIQNgtsSDy7q2KjqjHM-4dMVpPw/7zWJcpU4okg.jpg?size=636x420&quality=96&sign=13c8278b5b69e7852d357f4248c821e7&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-67.userapi.com/impg/huFBjufjFtL3_oL0LUuYzKT0w_FVw-DTSG0l1Q/FnWBwbm7WT4.jpg?size=733x260&quality=96&sign=ca1e9b54e6cb385cbed27b499f0ff206&type=album', stream=True).raw)
    im6 = Image.open(requests.get('https://sun9-74.userapi.com/impg/Aogn0JWgfdOrrfchwOHcY2wMt4Z604ldOoqgUg/THEWHtyRbtw.jpg?size=729x430&quality=96&sign=7627147852919b6ee92cf0a7daa5ed93&type=album', stream=True).raw)
    im7 = Image.open(requests.get('https://sun9-55.userapi.com/impg/t1dBypWAVOLLRnfx-0S8ko-OmrElNkSVeWaJzw/TcPdxpJTXbA.jpg?size=743x395&quality=96&sign=8329b6b11a0dd42076c46aef7439c3b9&type=album', stream=True).raw)
    return im1, im2, im3, im4, im5, im6, im7

#8
def pvoin_var_neizv_mu_b():
    im1 = Image.open(requests.get('https://sun9-61.userapi.com/impg/8VXWZRgz2jLb_l94w8AK8nIt1crKA6I1vHyITQ/Dpgub5gIrRg.jpg?size=734x469&quality=96&sign=764fe7361a142a484ce476541242a966&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-20.userapi.com/impg/_Cx7jSbsmPjTawZpc9q7Nr1Op-VvDbnmLl697g/0zq4K-FemGo.jpg?size=731x234&quality=96&sign=721b00d8e55b61d9a4cf2506aaca483a&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-72.userapi.com/impg/2pHRVbZUFF4XpAeQYGdoIH4roABtgHHAzIaC7A/fYBlpmqd3F4.jpg?size=532x643&quality=96&sign=3fa7d1f46f1a7e058aa6ea97c39cfbab&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-31.userapi.com/impg/t5w40UBXTyF6uIH_SXJDMPtg_59BdDBmvbIG8A/dVhuWaUaN4g.jpg?size=766x589&quality=96&sign=b791069490e99ce03d07e61729fed18b&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-54.userapi.com/impg/Ibk38I5fICAcJTpEZ99A-8KJat4zTm8mUiaxWQ/fBP9_y8lBuE.jpg?size=711x170&quality=96&sign=7c4842aa40c0fb306503c44d627a778c&type=album', stream=True).raw)
    im6 = Image.open(requests.get('https://sun9-56.userapi.com/impg/nTlJjf3AZ2QRE8GN8jXo1nimbIQpB1dbHrDMLQ/vGndEe77FzM.jpg?size=770x697&quality=96&sign=bc6a69301d43bc2802ffb76c7a9585c4&type=album', stream=True).raw)
    return im1, im2, im3, im4, im5, im6

#9
def pvoin_var_neizv_mu_m():
    im1 = Image.open(requests.get('https://sun9-2.userapi.com/impg/5FqHUfizwEEQQjp2vTbrJVUIxYtJ3St3W6Unkg/UgT6DkwJzfE.jpg?size=731x472&quality=96&sign=0d0b90c9fef2dbb772bf8ce1274a73b3&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-74.userapi.com/impg/LMrq0bXwovoghBb5lRgcYYA46LQVwFj6X_DNHw/dRc_-paV8sk.jpg?size=732x226&quality=96&sign=f3537b94b0008b2f1532f94111bb0be9&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-41.userapi.com/impg/2bjquNGioNAiZYvl2CVVIF3Z2A-Ukkfzoy_WJg/uGSXbRbU19A.jpg?size=730x475&quality=96&sign=d0d8006b06d0c6c99c94b3171963bd7d&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-75.userapi.com/impg/s_oLsfH0CV8HK5WG1LlCHJQa-qCD38uVtsmcEQ/q3EQMHWWp5g.jpg?size=692x174&quality=96&sign=46749559d628fdf1ffe1db3dad02f843&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-72.userapi.com/impg/2pHRVbZUFF4XpAeQYGdoIH4roABtgHHAzIaC7A/Oyr7RzWcoF4.jpg?size=532x643&quality=96&sign=0e533c745a5354c6b6186912f68f801e&type=album', stream=True).raw)
    im6 = Image.open(requests.get('https://sun9-49.userapi.com/impg/K9yBKVCD0-52ehWAnyihGBK13l55U8kCmiTJCA/cruBDj8atCU.jpg?size=895x427&quality=96&sign=e4f475ff4b895a2cc296c978d3a0187c&type=album', stream=True).raw)
    im7 = Image.open(requests.get('https://sun9-58.userapi.com/impg/yn6PiP8uxI-6nyuAi0d72SDPq3HEWq_s8Qg-2w/4Ui6E3hw45I.jpg?size=704x658&quality=96&sign=1587a785e45c95feb6684d7a6856e499&type=album', stream=True).raw)
    return im1, im2, im3, im4, im5, im6, im7

#10
def pvoin_var_neizv_mu_n():
    im1 = Image.open(requests.get('https://sun9-80.userapi.com/impg/MCoOjfXDC5ZsCXPyw6Q6dieQq0tjyKTmoRelqg/ck-p9Cz92kw.jpg?size=814x521&quality=96&sign=c918569704dbfa158e0f62d08f2ef3d5&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-47.userapi.com/impg/26PgZtbXzKxWPF7eMgy9IzyZPkx6VlaMdRLvEQ/iSr-MaLpJuo.jpg?size=1106x347&quality=96&sign=ba481a492621099e28f0442420582ffe&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-59.userapi.com/impg/-1_B5VAfPeCA2-72odKGISH6w-Dy-q856z_JzA/qLlvl-4M0tA.jpg?size=1008x649&quality=96&sign=d1ed16fdd4a17577e5af290ce9659b57&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-52.userapi.com/impg/Lc-Pm_7Iid3K8N5tzKiJJUcoKvh5NMTvBibxog/_N0PDtVf3nQ.jpg?size=962x247&quality=96&sign=5bd1d13dc30a75153f28e95dfc2916d3&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-72.userapi.com/impg/2pHRVbZUFF4XpAeQYGdoIH4roABtgHHAzIaC7A/3VWsTD8BL0g.jpg?size=532x643&quality=96&sign=da82049281b4e7636daa16046be2da23&type=album', stream=True).raw)
    im6 = Image.open(requests.get('https://sun9-70.userapi.com/impg/nXwOjql8tNPgdCUt42nCt7ux8gnnRXhDw1Gvcg/TXsYrCI_g6g.jpg?size=641x381&quality=96&sign=d5580a527e89858601fe841268346b4c&type=album', stream=True).raw)
    im7 = Image.open(requests.get('https://sun9-16.userapi.com/impg/IuR5cKNaZK4XidEeWUuJjcnEAwtBVjxkFQ7ZQw/TrBcKpVFvig.jpg?size=872x581&quality=96&sign=1ad152aa9acf8b8fdbe7a90cbc90e48a&type=album', stream=True).raw)
    im8 = Image.open(requests.get('https://sun9-42.userapi.com/impg/s4P-KP0V1NK-b-6FFXP-zVTVOPC376n6Co1UtQ/m7JNVU9Wj9E.jpg?size=875x295&quality=96&sign=0e77dd0c07f626be00041e387b36aaa8&type=album', stream=True).raw)
    return im1, im2, im3, im4, im5, im6, im7, im8

#11
def pvoin_mu_izv_var_b():
    im1 = Image.open(requests.get('https://sun9-1.userapi.com/impg/0khj54pbfvPnCxRqjypcFTzBGWL5iH_PUj-aZQ/XgiU-GI0uf8.jpg?size=838x710&quality=96&sign=35dc724763c177c753507d3525357ac2&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-46.userapi.com/impg/KtCeOJ5jVrm2SljKheFkScaYGXhxOEVO_UR7nQ/p2gH9XogKYc.jpg?size=1203x556&quality=96&sign=906fd0e9cc0b580c2af6adc2d61b8ecd&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-43.userapi.com/impg/9mVvfBsIR6AFFW_-0G7VyOv_UJR43bWD7TZiDQ/TAPBff3EEVs.jpg?size=831x293&quality=96&sign=e75514a119e05492977905f57fd4cb4e&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-26.userapi.com/impg/1Qtst9Rn4g4a-8A2BlC4JiJQOvZ1DboGYfNKRg/WX6yym-TyTY.jpg?size=1102x674&quality=96&sign=2df1200901900a38205e9202816154e1&type=album', stream=True).raw)
    return im1, im2, im3, im4

#12
def pvoin_mu_izv_var_m():
    im1 = Image.open(requests.get('https://sun9-67.userapi.com/impg/c9idpOuNHVeTd_5MkcX7gxXjR20BVu68kxlNAA/o4mBnevJiyA.jpg?size=888x602&quality=96&sign=07bbaddaac521b61d21ae5771fc64c41&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-9.userapi.com/impg/JevhWAJFl2DiaGrS7QP9wdqExIx9PhdgqWipsA/x_wf1ZW9lnk.jpg?size=882x254&quality=96&sign=d60f4f02ac0e05e1b9d963013beb05ac&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-62.userapi.com/impg/WMg808tpBb1FnbjksBUG8NURyAT9zOHGfgOh4g/yRAKhA9Y50Q.jpg?size=1277x435&quality=96&sign=6176b1fd348c2bded5ce32fcb40ee49e&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-24.userapi.com/impg/moi2fubWA3y72n6Ca5ed-n4MtPQLFiyWEVvwjw/HX3VdQecwEc.jpg?size=845x365&quality=96&sign=b3e7d705904080dac8094c2da466b27f&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-50.userapi.com/impg/r6Svzd25E_XTNRCKmlWPSGl9s3riUCLEgmF9Qw/WGOH828qqpo.jpg?size=1105x721&quality=96&sign=681825f67d88c821aa567574d05259b4&type=album', stream=True).raw)
    return im1, im2, im3, im4, im5

#13
def pvoin_mu_izv_var_n():
    im1 = Image.open(requests.get('https://sun9-72.userapi.com/impg/yq4GED6XXqNd29QTe283c4ToFSSaCnI4g1AYgQ/iGoZodL1Pto.jpg?size=886x593&quality=96&sign=e42398bfd160234f74701e7917610879&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-25.userapi.com/impg/oW59Ak4eCccXG04F-nRB3kfDOT9sIvgOLPKjyw/nW-cMNq4LN4.jpg?size=887x254&quality=96&sign=28b431198005db9c4f41d6738540b8a5&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-71.userapi.com/impg/CpBk2uFQIdd_5vDwKN2TYBj7O6euovD6jAUvnQ/XTThacNWHTE.jpg?size=1286x489&quality=96&sign=b11ba6cd4ec142c6bc41de7809da0230&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-20.userapi.com/impg/iHVThI_NIg-Sqvhsoseg6QN6WaMn6-HZwFcmYw/Agu0CoUTD5E.jpg?size=854x369&quality=96&sign=df236eb62a69311a474f2d2639817238&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-71.userapi.com/impg/YWxGlxTQLfiW0dCPaNCH1ACZ85wKCijo_vUD3A/YauZRwvP0dk.jpg?size=889x708&quality=96&sign=d9bbacb5417a9097e1e69867383a0a5f&type=album', stream=True).raw)
    return im1, im2, im3, im4, im5

#14
def pvoin_mu_neizv_var_b():
    im1 = Image.open(requests.get('https://sun9-7.userapi.com/impg/8NwmY1mEnl8GrztBclhScf4NvsnrLpueOC_RAA/7sk03dpdDCE.jpg?size=937x658&quality=96&sign=19099e91fea3105b2a3077349a10c79f&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-6.userapi.com/impg/AQY-b6c31UB7wL_wMXjnoWit8j-3T3dyjhrx5w/W0jrXq2hbt0.jpg?size=906x695&quality=96&sign=e0c67ebf398e2d53efa97dfbd72c4e43&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-80.userapi.com/impg/PgBNbTnBNiwgOWO9Y7V8P6_xItmyXSggio5v7w/ImUpgncSFAk.jpg?size=908x598&quality=96&sign=f6c20e5107ecddfdf8017f53aeb18751&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-51.userapi.com/impg/OYd5ckZq3sitrxVbWMuAKogS4TJETnr_80C7HA/iSFgzBL1bS4.jpg?size=935x673&quality=96&sign=5270a47ffba87e4ad824ee41b61b56a6&type=album', stream=True).raw)
    return im1, im2, im3, im4

#15
def pvoin_mu_neizv_var_m():
    im1 = Image.open(requests.get('https://sun9-2.userapi.com/impg/J53VgJFL6FV_WQLHLvIXMK3gvcJrlMfpXtyO0w/V-9o38VDB2A.jpg?size=954x663&quality=96&sign=6af0a97653cc8a16d63043b028a7021a&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-31.userapi.com/impg/gYBq9CiUUUhk5lIVvGTd5lwyWrwA-8Lg4UzH4g/wnTg4iZ6vSU.jpg?size=910x710&quality=96&sign=89d4c1d4aaf5d2103fd089737a543a3b&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-51.userapi.com/impg/zMnriXl-zl07cJX6Mp-Togg9THnxSYRMdmF-Wg/3S4-Br8EsXs.jpg?size=993x720&quality=96&sign=66943fe1623124e489b5ad77d783661c&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-74.userapi.com/impg/kmjYeb68yOG50zJE-jlbdMuyQkgp_ZCZuVbyww/Vx-IAjlZZMY.jpg?size=1003x699&quality=96&sign=5df082e332cdd0b96c753ded40def0e7&type=album', stream=True).raw)
    return im1, im2, im3, im4

#16
def pvoin_mu_neizv_var_n():
    im1 = Image.open(requests.get('https://sun9-29.userapi.com/impg/hF7YxNWXr6Z-Xc3UE45pTdHMYlVVNFqfaphvtg/plCdu1IRu1k.jpg?size=949x664&quality=96&sign=cf346fbaa346e5e556d12401d668b3dd&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-9.userapi.com/impg/2BJZzo0x_ID9L6NdHtYA_1qVOUluO4xCD0WmOQ/FIzVxFIZZyA.jpg?size=911x707&quality=96&sign=90e52c36f446e56df50903029f1ddd7a&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-63.userapi.com/impg/C1x2IyPA0en-FDgS_WG7lkOFrU0fWUrHsfQjyQ/GbbZOyFzzT4.jpg?size=1060x737&quality=96&sign=df37b7f41884f00431fcf802fcd47dc1&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-37.userapi.com/impg/pL7BcaH8YgkZMTDynT1h0eGTAyO5cfessBQm6w/Nmx1ogDM6sw.jpg?size=904x712&quality=96&sign=2d15bb054c2c2af0f3d89f117771e940&type=album', stream=True).raw)
    return im1, im2, im3, im4

#17
def pdnvo_var_izv_mu_b():
    im1 = Image.open(requests.get('https://sun9-46.userapi.com/impg/wAFsxdZybILpWC8oRAs5EF7NSdFKLfcB6IIdEA/rmHFUXoUlJU.jpg?size=900x645&quality=96&sign=b21cd876260ff5693324ec2999b6827b&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-43.userapi.com/impg/BU_5qVTxh9S_DsAINXnFLRiP2ivmMZ24kmNUBg/eNzA_my8CDE.jpg?size=1087x674&quality=96&sign=21292e2c9a589080a05aed0ff4add2d9&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-49.userapi.com/impg/q5-bWmJXUGICYthNNJp-INtCXl_RbElNNOQExQ/jKePD6_d_Cg.jpg?size=875x277&quality=96&sign=817733df4dbb2605567f136d135bc51d&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-11.userapi.com/impg/-U_mVLxCpAHWnvXrZxCDCT3y2hm6_Ria49S98A/Of1DTMoGsag.jpg?size=1059x702&quality=96&sign=d8f3b9ce84fdb6ef5ad21f04ef4f8298&type=album', stream=True).raw)
    return im1, im2, im3, im4

#18
def pdnvo_var_izv_mu_n():
    im1 = Image.open(requests.get('https://sun9-24.userapi.com/impg/v0BunzYN7tt37O9kzPY8TkdD_mzVkGQEJmRa8w/0b4DpkqbblM.jpg?size=905x742&quality=96&sign=fb0fcf36c394d1fff976c73f33c8f93b&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-8.userapi.com/impg/qAQ7P7dfT8ruacUNBVr5rPgvtdI7o3wXNFXMqQ/Y8P55vsQGEo.jpg?size=1081x672&quality=96&sign=df95d93edf39a036b493a61760881b89&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-60.userapi.com/impg/mz5iHehQ807VN8UpGrWlZMT0MpM3pYey4YR5cQ/ZUQHUlj0bQk.jpg?size=856x348&quality=96&sign=0dd5c27381f86892a9a8dc86605ea952&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-18.userapi.com/impg/cIf7fFkgum6teinPVVe2yODDoNaymtaOWoMkyw/lPlge-MfuLc.jpg?size=914x542&quality=96&sign=5f8f21e5ae1a2ea127e4619c511ca724&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-55.userapi.com/impg/9YxgkWX-baXHFbBUyjekeQBa4E88RC9koFSPxQ/zRqfs8Mm_eY.jpg?size=905x528&quality=96&sign=f81de22a288471f43ec6c6ee77f0e05b&type=album', stream=True).raw)
    return im1, im2, im3, im4, im5

#19
def pdnvo_var_neizv_ravn_mu_b():
    im1 = Image.open(requests.get('https://sun9-68.userapi.com/impg/IjScm4EmelZkTVQc3UP962J00V1Q98mzuPZD5w/Fewy2ydRp38.jpg?size=915x585&quality=96&sign=ffc46b0b793f85e3242d5637432645a8&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-75.userapi.com/impg/tbRHPongvdkK-HjstVaVmT8fmIuTR5x25zhCsg/8kwxeHQwaQc.jpg?size=914x667&quality=96&sign=40e21608601552155d63c9491263098d&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-16.userapi.com/impg/bV_CfuxWeDRLos02KmQS8iA6WUw8GG4Ghm_png/pNQGE_tusng.jpg?size=758x490&quality=96&sign=a7b4c8ea020b1c8d7a11e8b56e19e480&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-63.userapi.com/impg/iYEnpUwbFMO6QpytJ2QJqKc7RpLM9a6NUsIvAA/2jppxR4KohA.jpg?size=736x235&quality=96&sign=2ee560d3669e15a06e9145581fc9c15c&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-60.userapi.com/impg/QA05GgER1S84eK7OK8fQSrvWFBqlM042aFd8Ew/t6Hwvela_io.jpg?size=915x143&quality=96&sign=af8e1bc4b8ce61265a85f2471749c24c&type=album', stream=True).raw)
    im6 = Image.open(requests.get('https://sun9-6.userapi.com/impg/yzy1MhRyswwwhnwANq8A-OJwchlaM1bV7gmwYA/e358Q-dQAYQ.jpg?size=719x316&quality=96&sign=ee8975c9edfaef55bc4b9461c148c76a&type=album', stream=True).raw)
    im7 = Image.open(requests.get('https://sun9-3.userapi.com/impg/8IYDyLTfsbKnQFZOm2qH-1DHGe1m3dYps6vblw/dCr6YBz2EWk.jpg?size=917x526&quality=96&sign=8c4613d03cf738887e11471e63146b63&type=album', stream=True).raw)
    im8 = Image.open(requests.get('https://sun9-6.userapi.com/impg/yzy1MhRyswwwhnwANq8A-OJwchlaM1bV7gmwYA/LI8fiVd46Yk.jpg?size=719x316&quality=96&sign=22cd440158621b4bdbcbce95bd607133&type=album', stream=True).raw)
    return im1, im2, im3, im4, im5, im6, im7, im8

#20
def pdnvo_var_neizv_ravn_mu_n():
    im1 = Image.open(requests.get('https://sun9-48.userapi.com/impg/ZwU9ivfsC8R0CzZw5KAN0zRJ1TO8JCPHv_QiEA/goaGz-ChUGU.jpg?size=913x585&quality=96&sign=019b38db947388a4664a0c9196319746&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-61.userapi.com/impg/PdJGkS7wkGAe2ySFRmTXkjUATMlGzAHymymn3A/2Obg-2SABBU.jpg?size=912x662&quality=96&sign=62ba2b87e0d9d63944eef92e5910125b&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun1-16.userapi.com/impg/bV_CfuxWeDRLos02KmQS8iA6WUw8GG4Ghm_png/_7fLRqWC4_w.jpg?size=758x490&quality=96&sign=607614e7e95c71348a662321db96ba40&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-63.userapi.com/impg/iYEnpUwbFMO6QpytJ2QJqKc7RpLM9a6NUsIvAA/SZpKMb47SH8.jpg?size=736x235&quality=96&sign=d5183eddd32360bc6941e0ad89603f17&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-71.userapi.com/impg/Uix4Rnte8Af7NEwfMM1d7euCInU6vPDmg1YEGg/-QSAHa5rOG4.jpg?size=542x81&quality=96&sign=1a6445221dfa3d4f8f92296f9f4a764e&type=album', stream=True).raw)
    im6 = Image.open(requests.get('https://sun9-25.userapi.com/impg/6zfKsvcIgha9NBQZw9e7S2RX43dTwWAO2Nb4Vg/QZSYNvcyuxs.jpg?size=668x243&quality=96&sign=d871b9c4151e75b549a09f5eb9651b23&type=album', stream=True).raw)
    im7 = Image.open(requests.get('https://sun9-25.userapi.com/impg/LfzBrvtuSCyjPWsyzh5TSR4sZRKlAxg3nSo34g/qMZCyI7xkKs.jpg?size=535x314&quality=96&sign=53db73bac83d5193a896326c3ff13e94&type=album', stream=True).raw)
    im8 = Image.open(requests.get('https://sun9-60.userapi.com/impg/Qau9uevEO4pcCVF_0fIN8gspNZ5eQzZ3-o2axw/BSAMIj5ECqM.jpg?size=540x342&quality=96&sign=385dd5f95b12a907bef13bea0f16d8cb&type=album', stream=True).raw)    
    return im1, im2, im3, im4, im5, im6, im7, im8

#21
def pdnvo_var_neizv_neravn_mu_n():
    im1 = Image.open(requests.get('https://sun9-19.userapi.com/impg/9O7CaNHuG5XaKY-BNySI6J6f4AAsGz6SumO7qw/HFwy_mDZ5Rs.jpg?size=912x713&quality=96&sign=006b5ae82ba8205c2c72d721ed235f44&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-3.userapi.com/impg/UiHGak0lptKtF5qUasJX3FDQrn0NG7t4jta5gA/Im_SyOLr3Sg.jpg?size=539x276&quality=96&sign=f6f5f8bfad07b276b3d5bd3a1ceeceab&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-74.userapi.com/impg/InoJdhijl8wbTSLviXc6GkY9tNxcO-m-eBMN1g/XUU6rJ7_luw.jpg?size=915x628&quality=96&sign=8d56a5e5c74d834b6e12508c8586e974&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-53.userapi.com/impg/WH2W1YfwK-8-MGW4tmaoiCwjSxfbzpaUsP54oA/1lVbnmairjY.jpg?size=539x309&quality=96&sign=8f8b4f6ca591b439978ca905bdbdfa26&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-7.userapi.com/impg/vRzeUjdJI-cPZiHXM83qtT7-0D6iU_4-dBbmqg/M2JFQfAKT3Q.jpg?size=726x135&quality=96&sign=45fffba1644c04474210ff1a9ac18c9b&type=album', stream=True).raw)
    return im1, im2, im3, im4, im5

#22
def pdnvo_var_b():
    im1 = Image.open(requests.get('https://sun9-32.userapi.com/impg/OD51iBtswu3IPUXtZ6Ded1bz30IiE-ryMqxeMw/w2zOEz61kzE.jpg?size=957x740&quality=96&sign=cd213ff17088d7e37ad2fd126d832fd2&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-68.userapi.com/impg/ovSfdtB9KHawy7SKN-Kw5cJtYimZ8W_VrRTfWg/ReKZpP3oeWQ.jpg?size=917x626&quality=96&sign=c53d6efba2ffa8dea06b25cf84606c71&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-11.userapi.com/impg/AYYsstnY7NL3iQ8Uq0FMhTTEvVPKdQ9wHJ3qAA/EIsr8hpX5hg.jpg?size=914x473&quality=96&sign=2a4134034959e9290501cf02eeb3f7f6&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-4.userapi.com/impg/YEUMXsFpQDeUz8sMfAfWdVNxeeCamSvBmV4j7g/kRbE8AXqzMA.jpg?size=1135x385&quality=96&sign=f756569cdc7b31241c3013b58bae81a0&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-73.userapi.com/impg/UoAEEhVzf7Yf7ur1dnoVh89uwZKD3BGP9uXhAw/cuJrdX_KWtg.jpg?size=537x256&quality=96&sign=e160de878f6282ca6becd6c1b64343b6&type=album', stream=True).raw)
    im6 = Image.open(requests.get('https://sun9-30.userapi.com/impg/L-EjEBCp9ScgK0NDQTAm4o4K7A9xFETHQoB41w/9y1MPyaxVRA.jpg?size=1196x648&quality=96&sign=efbe14cedc504c564eaf2604aa715304&type=album', stream=True).raw)
    return im1, im2, im3, im4, im5, im6

#23
def pdnvo_var_n():
    im1 = Image.open(requests.get('https://sun9-68.userapi.com/impg/ytxoTXdc2WLMLB4zLyBSg4zyt0MaAdRv9MkJFg/mqTKqXHZrZU.jpg?size=972x759&quality=96&sign=837da2bcfb94396c6970445c1c5d666c&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-31.userapi.com/impg/k4AcOVOiSXC_chve5oC7jpm6s2EmHRcbpfPurw/Kyr8o0uJ6E0.jpg?size=933x645&quality=96&sign=31a3d005480964177abf45e8f405ccc0&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-49.userapi.com/impg/Z8yOby2zdIZAFN4J_f8s2s58Qb3KXC2MjHahOQ/TYw3mItSL_o.jpg?size=940x482&quality=96&sign=1ba493d9665607066c037b7c7fe83a6d&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-31.userapi.com/impg/fmYxM2WXiZimIexy8ptEaFt9kPasqJpeg5oqhQ/HUbuospsCcI.jpg?size=1238x499&quality=96&sign=f52413c1e40a5155f640a8f6bbae67ca&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-80.userapi.com/impg/s2yQrwe9i2ccHp3-oQGLtKvk159w6h6oS2Cwxw/CgxNcsGhplo.jpg?size=644x712&quality=96&sign=4871a130fba46f59e7f4607e90f308b7&type=album', stream=True).raw)
    im6 = Image.open(requests.get('https://sun9-5.userapi.com/impg/A9ZpJRCUch3fpW7InqRC50MyUwvqBXFjnIIwHg/U449RgZmDq0.jpg?size=848x515&quality=96&sign=b98fc9153b2f0caa1182e14b5853639e&type=album', stream=True).raw)
    return im1, im2, im3, im4, im5, im6

#24
def pdnvo_var_neizv_ravn_mu_n_F():
    im1 = Image.open(requests.get('https://sun9-32.userapi.com/impg/-1OgFWzuxC_23OfFOqcho6UNV4YuOT3-fZXe5g/uXHO4Lm1u3g.jpg?size=534x347&quality=96&sign=2ed0c324f6124cc040877bcf0cef16aa&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-38.userapi.com/impg/WdK97hTlYIYvKEiof-xQkXCiv6UXlTYCMuTl6w/04tIx8dykXU.jpg?size=487x627&quality=96&sign=33668c7149b47df2ef03146439eca896&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-13.userapi.com/impg/6xdzL4KHuhnKkdhF28KKjEk4DDP8vTZoMeT3Rg/NnnV4s74i5c.jpg?size=652x348&quality=96&sign=cc93b0f5453770b3b834761d0e9f103c&type=album', stream=True).raw)
    return im1, im2, im3


#Q3
#1
def pvirrno():
    im = Image.open(requests.get('https://sun9-37.userapi.com/impf/YMPZ1iGgOt99wBbNXwZR7qOIPnCFdPgRSevBhw/bQ7GIN2Yddk.jpg?size=1642x731&quality=96&sign=a8ca5d8442368ad26d2e517f48b371f2&type=album', stream=True).raw)
    return im

#2
def ivoig():
    im = Image.open(requests.get('https://sun9-31.userapi.com/impf/SaZxdvKQSEZcM3iufaIdP_nCAHhZVIye8ndNxA/Z7KHR8Y92P8.jpg?size=1954x494&quality=96&sign=32c3b17f514c708fc767f4dc55cb7c5e&type=album', stream=True).raw)
    return im

#3
def pidnn():
    im = Image.open(requests.get('https://sun21-2.userapi.com/impf/6TK1ppPmMAyb6CmrzYJpG49hSu6HJba9cqZ0GQ/0AzHamaEXlw.jpg?size=1535x646&quality=96&sign=31f726dbe94f89cb46b008a0e06f0da3&type=album', stream=True).raw)
    return im

#4
def popas():
    im = Image.open(requests.get('https://sun9-29.userapi.com/impf/gBV64edyLbEFpJMvgIj9TlwPFXnzlP-kryDL8g/M6PZVs65hm4.jpg?size=1442x409&quality=96&sign=dc3d87663b88b89fe286acf592642328&type=album', stream=True).raw)
    return im

#5
def pvoinrsg():
    im = Image.open(requests.get('https://sun9-78.userapi.com/impf/4swn498xizahuyRhFU5LeCqKaZSXJJ3vHUftcg/x-iJX0g5CK4.jpg?size=1674x1320&quality=96&sign=7ac11f1e5622ab21cec6769f9418b4f5&type=album', stream=True).raw)
    return im

#6
def pvoirsm():
    im = Image.open(requests.get('https://sun9-56.userapi.com/impf/Hq8MYGxztC4cZXXpoRrx3epnWZs3CChyJrr2Ew/tfckvAr3osw.jpg?size=1398x1212&quality=96&sign=e0aec428463627bbd1d252f765d2e823&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-30.userapi.com/impf/vEJxYWAoB38__v74s25sT-ZSnP0OuyVU4KguoQ/euuL-JYAysc.jpg?size=1529x1015&quality=96&sign=4c6a843cd2872430b9aba9e9915468c4&type=album', stream=True).raw)
    return im, im2

#7
def pvigrsmo():
    im = Image.open(requests.get('https://sun9-30.userapi.com/impf/3BCKyKrGHL5GWXUhRG0jPPgFPwPD5s5xUh0JrQ/P_MoYIxbuSM.jpg?size=1558x1009&quality=96&sign=ac2dd190d13b623ca36e2ffc9c787e73&type=album', stream=True).raw)
    return im

#8
def pvird():
    im = Image.open(requests.get('https://sun9-76.userapi.com/impf/6IAFyvc-7BE5TnhuB1z9iw7Lnpbiip7FhbBupA/ELWflU9C5Lo.jpg?size=1086x1201&quality=96&sign=bcab7b8408a9c1d9620fec5eb29c7be1&type=album', stream=True).raw)
    return im

#9
def pvigri():
    im = Image.open(requests.get('https://sun9-22.userapi.com/impf/SX_eyBtp6nDf-I-OE_CWwU8DVrwBfesoriUyTA/mob_K_dHSls.jpg?size=982x1057&quality=96&sign=64babec8a6331ece9d4f24eb8d57c297&type=album', stream=True).raw)
    return im

#10
def pvirr_drob():
    im = Image.open(requests.get('https://sun9-7.userapi.com/impf/kG1n1-gOtHSChIkEEj0p9usjDN5xvobkLkUoJw/XYnfyzSNxfw.jpg?size=930x1092&quality=96&sign=c12e7d2105cacec5320b09308b522f74&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-40.userapi.com/impf/W39MspQ3nE6V1rJvjdStpBmq7DVqUJ96Xy5JUA/-K7uLWvkZiE.jpg?size=1373x742&quality=96&sign=ee870f4e39db27d98eefd4961d3cbb02&type=album', stream=True).raw)
    return im, im2

#11
def pvirr_umnozh():
    im = Image.open(requests.get('https://sun9-70.userapi.com/impf/paPd7GgTEogvFzdvtfPvfaSo33BbPZH-UIrHdA/pgiY0shx4g0.jpg?size=1352x1297&quality=96&sign=02dcce30f8f39568887f1d196e5ce188&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-79.userapi.com/impf/apHnmoJjfLfJuTrFitBUe4Fu9tQ8YTETq65glw/l9QxhF-MODk.jpg?size=1578x1349&quality=96&sign=abb3dcb76380c1ee104f706c1178ddba&type=album', stream=True).raw)
    return im, im2

#12
def psvki():
    im = Image.open(requests.get('https://sun9-22.userapi.com/impf/YNffmr6ApW3xv3NjNJJIuF3CbJuSHM4xJJ4VJw/PFeyDP0yo6k.jpg?size=1363x776&quality=96&sign=865c3af16d02af09675717f5ab1aff0e&type=album', stream=True).raw)
    return im

#13
def pvoirz():
    im = Image.open(requests.get('https://sun9-10.userapi.com/impf/SuhYWvSc9yAFikj_5FCWXmN3-iHPDGkfUom8TA/Bs1tk6a51Sk.jpg?size=1240x896&quality=96&sign=4d868abce467d468af91381c660aa758&type=album', stream=True).raw)
    return im

#14
def pgnka_bez_skob():
    im = Image.open(requests.get('https://sun9-66.userapi.com/impf/A4xD2BSncmKduVnfEfRqlZ5X28pqedr40Ln4Xg/KBoSrSFddYY.jpg?size=1934x584&quality=96&sign=9ffbf2ce38887ea0186303845fd64391&type=album', stream=True).raw)
    return im

#15
def pgnka_so_skob():
    im = Image.open(requests.get('https://sun9-10.userapi.com/impf/p8kngBBp7RNs9jIusGwON-APp2SOkZATdFiTuQ/3J130FpHlG8.jpg?size=2189x644&quality=96&sign=e9f115ecc4ede3114b2f422b01236e9f&type=album', stream=True).raw)
    return im

#16
def vtpdp():
    im = Image.open(requests.get('https://sun9-79.userapi.com/impf/Hy3Bx6erlsHToAsdmVzHhFH-CUo0_YcXvjQPQg/9eBurwHO_Q8.jpg?size=1643x772&quality=96&sign=f6bc27e498b0513e90cea5eb8c94ecf0&type=album', stream=True).raw)
    print('''
xi = np.array([i for i in range(11)])
ni = np.array([146, 97, 73, 34, 23, 10, 6, 3, 3, 3, 2])
#a
mu = np.dot(xi, ni)/sum(ni)
lambda_ = mu
print(mu)
p = 1 - (lambda_**(0) * np.exp(-lambda_) / 1) - (lambda_**(1) * np.exp(-lambda_) / 1) - (lambda_**(2) * np.exp(-lambda_) / 2)
print(p)
#б
p_ = ni[xi >= 3].sum()/sum(ni)
print(p_)
    ''')
    return im

#17
def psvrrno04():
    im = Image.open(requests.get('https://sun9-27.userapi.com/impf/1kFvuE-ONy7l1p9Quuz4C194TgjC_Bl9dWbgJA/0cWk-2gDwfo.jpg?size=1325x1431&quality=96&sign=dc7364ca1f00e905a1fdd4430efca840&type=album', stream=True).raw)
    return im

#18
def psvrrnoab():
    im = Image.open(requests.get('https://sun9-80.userapi.com/impf/etxuLkKCGfccC31DlEUOpzfWu8sXcZeQruVOlA/LDkh2vLZXwQ.jpg?size=1509x1249&quality=96&sign=fc49a70f93969e741efe094cc827ca5b&type=album', stream=True).raw)
    return im

#№19
def svssi():
    im = Image.open(requests.get('https://sun9-79.userapi.com/impg/dgRD_qIgrnAcE8JL81mZ9KoVJqaQsxHFrfCBcw/X3rvf_1Y-TY.jpg?size=179x162&quality=96&sign=935586437d20355c3daab768d838c02d&type=album', stream=True).raw)
    print('''xi = np.array([4.55, 11.55, 18.55, 25.55, 32.55, 39.55, 46.55, 53.55, 60.55])
ni = np.array([219, 98, 50, 25, 17, 7, 2, 4, 1])
nu_1 = np.dot(xi, ni)/sum(ni)
nu_2 = np.dot(ni,(xi-nu_1)**2)/sum(ni)
print(nu_1, nu_2)

lambda_, tau, x = sp.symbols('lambda, tau, x')
eq1 = sp.Eq(1/lambda_ + tau, nu_1)
eq2 = sp.Eq(1/lambda_**2, nu_2)
otv = sp.solve((eq1, eq2), (lambda_,tau))
lambda_ = round(otv[1][0],4)
tau  = round(otv[1][1],4)
print(lambda_, tau)

class shifted_exponential_distribution(sts.rv_continuous):
    def _pdf(self, x):
        lambd = 0.0992
        t = 1.4873
        if x >= t:
            return lambd * np.exp(-lambd * (x - t))
        return 0
    
X = shifted_exponential_distribution()
Time = X.ppf(0.9066)
print(Time)
#p.s. в условии ответ для времени неправильный''')
    return im

#20
def ichdvp():
    print('''x, b = sp.symbols('x b')
f = b * x**(b-1)
print(sp.integrate(x * f, (x, 0, 1)).simplify()) #лучше вывести без print
b = list(sp.solve([b/(b+1) - 0.78]).values())[0]
print(b)

class distribution(sts.rv_continuous):
    def _pdf(self, x):
        if 0 <= x <= 1:
            return b*x**(b-1)
        else:
            return 0
X = distribution()
proba = X.cdf(0.67)
print(proba)''')
    im = Image.open(requests.get('https://sun9-21.userapi.com/impf/e7SXJXVzZR0HSFSQ1HLMCCCdTjWnC49DOiHnFg/Kx0_28UUUI8.jpg?size=645x578&quality=96&sign=d56bdf4cb4a4f653a2edd82026085728&type=album', stream=True).raw)
    return im

#21
def pvoirp():
    im = Image.open(requests.get('https://sun9-35.userapi.com/impg/aTpNjvU3E0pskojItHgNkEA93KTFtXseqbBv-w/hY6wUmm-0dM.jpg?size=593x606&quality=95&sign=f009c7bbfd60aa0e30bd3c6c86e1e851&type=album', stream=True).raw)
    return im

#22
def nmmpp():
    im = Image.open(requests.get('https://sun9-59.userapi.com/impg/SIq3p-ji0lTHEa6jfkYrB_Zt6HnpyuYNSBdDbw/Yef85-ORV8g.jpg?size=729x345&quality=95&sign=bb449f58507f7d0c824ae102f0c2740d&type=album', stream=True).raw)
    return im

#23
def nopip():
    im1 = Image.open(requests.get('https://sun9-27.userapi.com/impg/Tl89eZujOMuJO74L7iqEGZO7zvG3qWqo8aLoTw/_LiDjVNu-C0.jpg?size=567x490&quality=95&sign=874341ed024bbb4ffdab112922508cea&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-17.userapi.com/impg/4mYO-wdqE7Zi_Jz5miWhMztuilTXgQRazuLOcw/wTPCpQ-Znks.jpg?size=591x208&quality=95&sign=1019f3287c1575140cd521cab8143f20&type=album', stream=True).raw)
    return im1, im2
    
#24
def pvidr():
    im = Image.open(requests.get('https://sun9-78.userapi.com/impg/1iPHjxfUV8h737JGWeszJXzNYyMRvqKA1rX_Dg/2oJ4zWHdCUs.jpg?size=571x759&quality=95&sign=55cf09af99b468c08ee347736716eaf2&type=album', stream=True).raw)
    return im

#25
def pochss():
    print('''n,m,a,b = sp.symbols('n,m,a,b')
f = (a/n + b/m)**2 / (a**2/(n**2*(n-1)) + b**2/(m**2*(m-1)))
# sp.factor(f-(n+m-2)) напечатать в отдельные ячейки
# sp.factor((n-1)-f)
# sp.factor((m-1)-f)''')
    im = Image.open(requests.get('https://sun9-33.userapi.com/impg/Mdjn57HKGLbc2YgMOj7qynYTqeuMQEayejvdFA/d34YTzrPoKs.jpg?size=611x779&quality=95&sign=afec411c8fb3ed400cc92e0e5dd1b37c&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-14.userapi.com/impg/eq-WQqek7Q5j6PF2jmsPVzr_1zQBYQjxptamVA/c12cb3t2vDo.jpg?size=610x516&quality=95&sign=0b7bced22e24ea3bf78beec932d7d67c&type=album', stream=True).raw)
    return im, im2
        
#26  
def pvptr():
    im = Image.open(requests.get('https://sun9-63.userapi.com/impg/hv-Db3YgHO8m1oED6-2CLtPkrpoup95z9NQWjA/X83pZnUqSls.jpg?size=633x418&quality=95&sign=ff4b279e50389ccf3f912194227467e3&type=album', stream=True).raw)
    return im

#27
def inzkk():
    print('''n = 100
ni = np.array([26, 25, 29, 20])
p = np.array([1/4]*4)

chi2_obs = sum(((ni - n*p)**2)/(n*p))
chi2_cr = sts.chi2.isf(0.01, 3)
print(chi2_obs, chi_cr)
print('H0 отвергаем') if (chi2_obs > chi_cr) else print('H0 не отвергаем')''')
    im = Image.open(requests.get('https://sun9-58.userapi.com/impg/dr4rMqiGB0kvs5OvV7WfMNU1xjITL9w3040tSg/sBpQDx_xws4.jpg?size=362x99&quality=96&sign=926ac878b148983af6f0c04856964749&type=album', stream=True).raw)
    return im

#28
def vdzchs():
    print('''ni_obs = np.array([968,1026,1021,974,1012,1047,1022,970, 948, 1014])
alpha = 0.05
n = sum(ni_obs)

l = len(ni_obs)
pi=np.array([1/l]*l)
ni_exp=n*pi
chi2_cr = sts.chi2.isf(alpha, l-1)
chi2_obs=sum((ni_obs-ni_exp)**2/ni_exp)
print(chi2_obs, chi_cr)
print('H0 отвергаем') if (chi2_obs > chi2_cr) else print('H0 не отвергаем')

p_val = sts.chi2.sf(chi2_obs,l-1)
print(p_val)

print(sts.chisquare(ni_obs))#проверка''')
    im = Image.open(requests.get('https://sun9-58.userapi.com/impg/dr4rMqiGB0kvs5OvV7WfMNU1xjITL9w3040tSg/sBpQDx_xws4.jpg?size=362x99&quality=96&sign=926ac878b148983af6f0c04856964749&type=album', stream=True).raw)
    return im
    
#29
def sschchn():
    print('''#по идее в задаче опечатка, альфа должно быть 0,01
alpha = 0.01
l = 2
n = 10000
k = 5089

ni_obs = np.array([k,n-k])
pi=np.array([1/l]*l)
ni_exp=n*pi
chi2_cr = sts.chi2.isf(alpha, l-1)
chi2_obs=sum((ni_obs-ni_exp)**2/ni_exp)
print('H0 отвергаем') if (chi2_obs > chi2_cr) else print('H0 не отвергаем')

p_val = sts.chi2.sf(chi2_obs,l-1)
print(sts.chisquare(ni_obs,ni_exp))#проверка

print('при alpfa > 0.075076 (смотрим по p_val) эта гипотеза отвергается')''')
    im = Image.open(requests.get('https://sun9-58.userapi.com/impg/dr4rMqiGB0kvs5OvV7WfMNU1xjITL9w3040tSg/sBpQDx_xws4.jpg?size=362x99&quality=96&sign=926ac878b148983af6f0c04856964749&type=album', stream=True).raw)
    return im

#30
def pnisi():
    print('''theta = sp.symbols('theta')
n = 8002
obs = np.array([2014, 5008, 980])
p_hat = obs / n
p_exp = np.array([0.5 - 2 * theta, 0.5 + theta, theta])
l = 3
alpha = 0.05
#_____
chif = np.sum(n / p_exp * (p_hat - p_exp) ** 2)

#графики лямбда-функции
t = np.linspace(0.1, 0.24, 10000)

fig, ax = plt.subplots(1, 2, figsize=(15, 8))

ax[0].plot(t, sp.lambdify(theta, chif)(t), c='blue')

ax[1].plot(t, sp.lambdify(theta, chif)(t), c='blue')
ax[1].set_ylim(0.15, 0.25)
ax[1].set_xlim(0.122, 0.126)
ax[1].plot(0.12371709, 0.18316062973803104, 'ro', markersize=10, mec='black')

ax[0].grid(linestyle='--', alpha=0.4)
ax[1].grid(linestyle='--', alpha=0.4)

plt.show()
#__________________

from scipy.optimize import minimize
minimize(sp.lambdify(theta, chif), (0.1235), method='Nelder-Mead')#вывести отдельно
#______
chi2a = sts.chi2.isf(alpha, l - 1 - 1)
print(chi2a)
#_______
chif = sp.lambdify(theta, chif)(0.12371709)
print(chif)

print('H0 отвергаем') if (chif > chi2a) else print('H0 не отвергаем')

# необязательно
pv = sts.chi2.sf(alpha, l - 1 - 1)
print(pv)
sts.chisquare(obs, n * np.array([0.5 - 2 * 0.12371709, 0.5 + 0.12371709, 0.12371709]), ddof=1)''')
    im = Image.open(requests.get('https://sun9-4.userapi.com/impg/lhfbW75M_3REu-_JtlX6u7-Y258L2-A555ZiBw/F02xOAPIW-8.jpg?size=686x555&quality=96&sign=3b3dd1358e027ad3bda1a7aa9adf1091&type=album', stream=True).raw)
    return im

#31
def ptsdp():
    print('''a, b, c, d,n = sp.symbols('a,b,c,d,n')
chi2 = n*((a**2*(b+d)*(c+d) + b**2*(a+c)*(c+d) + c**2*(a+b)*(b+d) + d**2*(a+c)*(a+b))/((a+c)*(a+b)*(b+d)*(c+d)) - 1)
chi2.factor()''')
    im = Image.open(requests.get('https://sun1-21.userapi.com/impg/S_FO3NrYNlWuMU1gzTSFV_pYiLYBjpy5TpRozA/A7kgw4KsGZg.jpg?size=612x717&quality=95&sign=8a77308c0f62a17dffe247220bbf9266&type=album', stream=True).raw)
    return im

#32    
def chdzpzchi2():
    print('''PI = '141592653589793238462643383279'
PI_list = np.array(list(map(int, list(PI))))
E = '718281828459045235360287471352'
E_list = np.array(list(map(int, list(E))))

alpha = 0.05
n1 = len(PI_list)
n2 = len(E_list)
print(n1, n2)
l = len(PI_ni)

PI_ni = np.array([PI.count(str(i)) for i in range(10)])
E_ni = np.array([E.count(str(i)) for i in range(10)])

mui, vi = PI_ni, E_ni

chi2_obs = sum((mui - vi)**2 / (mui+vi))
chi2_cr = sts.chi2.isf(alpha, l-1)
print(chi2_obs, chi2_cr)

print('H0 отвергаем') if (chi2_obs > chi2_cr) else print('H0 не отвергаем')''')
    im = Image.open(requests.get('https://sun9-80.userapi.com/impg/Tg707q5EV0WBKo6N--_7yf8s2L54utS1QbnWLQ/OJsodkG3-4E.jpg?size=691x557&quality=96&sign=2844ee0ffb5026b4d143ed0194a1b822&type=album', stream=True).raw)
    return im

#33
def itschv():
    def itschv():
    print('''
#неправильное    
n = 150
ni_obs = np.array([16, 15, 19, 13, 14, 19, 14, 11, 13, 16])
X = np.array(sum([[i] * ni_obs[i] for i in range(10)], []))

Dn = max([max(abs(sts.uniform.cdf(X[i-1]) - (i - 1) / n), abs((i / n) - sts.uniform.cdf(X[i-1]))) for i in range(1, n+1)])
print(Dn)
#проверка
print(sts.ks_1samp(X, sts.uniform.cdf))

lambda_n = np.sqrt(n)*Dn
lambda_cr = sts.kstwobign.isf(0.01)
print(lambda_n, lambda_cr)

print('H0 отвергаем') if (lambda_n >= lambda_cr) else print('H0 не отвергаем')


# решение Рябова
from scipy.optimize import minimize

nk=np.array([16,15,19,13,14,19,14,11,13,16])
n=sum(nk)
pk=nk/n
w=[]

for i in range(1,11):
    w.append(sum(pk[:i]))
print(w)

xk=np.array([9/2,(10+19)/2,(20+29)/2,(30+39)/2,(40+49)/2,(50+59)/2,(60+69)/2,(70+79)/2,(80+89)/2,(90+99)/2])
pk=nk/n

W=sts.rv_discrete(values=(xk,pk))
sigma_hat=W.var()+9**2/12
a_hat=W.mean()-np.sqrt(3)*W.std()
b_hat=W.mean()+np.sqrt(3)*np.sqrt(sigma_hat)

a=0
b=98.5
#b=98.498
#b=98.49772797419996
#b=98.497727
#b=b_hat
loc=a
scale=b-a
X=uniform(loc,scale)

y = np.vectorize(Fecdf0, otypes=[float])

def f(x):
    return -abs(y(x)-X.cdf(x))

def Fecdf0(x):
    if 0<=x<=9:
        return (w[0])/9*(x)
    if 9<=x<=10:
        return w[0]
    for i in range(1,10):
        if 10*i<=x<=10*i+9:
            return w[i-1]+(w[i]-w[i-1])/9*(x-10*i)
        elif 10*i+9<=x<=10*(i+1):
            return w[i]
        elif 100<=x:
            return 1
        
res=minimize(f, 59, method='Nelder-Mead', tol=1e-10)
ymax=-res.fun
xmax=res.x[0]

d0=abs(X.cdf(xmax)-Fecdf0(xmax))
K=sts.kstwobign()
alpha=0.01
calpha=K.isf(alpha)

n=sum(nk)
Dn=np.sqrt(n)*d0
print(Dn)

PV=K.sf(Dn)
print(PV)
''')
    im = Image.open(requests.get('https://sun9-64.userapi.com/impg/EknQseNeW1_KinjyR4dxb3kGxm2ykt1HIaPgqw/gdEJyL1BNS4.jpg?size=696x275&quality=96&sign=7c219fd0ff393921e8d4cdfe9ef916b4&type=album', stream=True).raw) 
    return im

#34
def chdzpzks():
    print('''PI = '141592653589793238462643383279'
PI_list = np.array(list(map(int, list(PI))))
E = '718281828459045235360287471352'
E_list = np.array(list(map(int, list(E))))

alpha = 0.05
n1 = len(PI_list)
n2 = len(E_list)

PI_ni = np.array([PI.count(str(i)) for i in range(10)])
E_ni = np.array([E.count(str(i)) for i in range(10)])

PI_cdf = np.array([sum(PI_ni[0:i+1]) / n1 for i in range(len(PI_ni))])
E_cdf = np.array([sum(E_ni[0:i+1]) / n2 for i in range(len(E_ni))])

D = max([abs(PI_cdf[i] - E_cdf[i]) for i in range(len(PI_cdf))])
print(D)
#проверка
print(sts.ks_2samp(PI_list, E_list, method='asymp'))

D_obs = np.sqrt(n1 * n2 / (n1 + n2)) * D
k = sts.kstwobign.isf(alpha)
print(D_obs, k)

print('H0 отвергаем') if (D_obs > k) else print('H0 не отвергаем')''')
    im = Image.open(requests.get('https://sun9-36.userapi.com/impg/m_nnn3p_HD-_nfXKVLY40d8QO0NSwGXyR7F5aw/kxaaniSu1Os.jpg?size=702x326&quality=96&sign=035b5144d45bffe936c74dc6d7876f02&type=album', stream=True).raw)
    return im

#35
def svichb():
    print('''table = np.array([[60,54,46,41],[40,44,53,57]])
n = np.sum(table)
alpha_1 = 0.05
alpha_2 = 0.025
mu_i = [sum(j) for j in table]
nu_j = sum(table)
r = len(mu_i)
s = len(nu_j)
chi2_obs = n * (sum([table[j][i]**2 / (mu_i[j]*nu_j[i]) for j in range(r) for i in range(s)]) - 1)
chi2_cr = sts.chi2.isf(alpha_1, (r-1)*(s-1))
print(chi2_obs, chi2_cr)
p_val = sts.chi2.sf(chi2_obs, (len(mu_i)-1)*(len(nu_j)-1))
print(p_val)
print('H0 отвергаем') if (chi2_obs > chi2_cr) else print('H0 не отвергаем')
print('H0 отвергаем') if (p_val < alpha_1) else print('H0 не отвергаем')

#__________
chi2_cr = sts.chi2.isf(alpha_2, (r-1)*(s-1))
print(chi2_cr)
print('H0 отвергаем') if (chi2_obs > chi2_cr) else print('H0 не отвергаем')
print('H0 отвергаем') if (p_val < alpha_2) else print('H0 не отвергаем')''')
    im = Image.open(requests.get('https://sun9-12.userapi.com/impg/aI_ZeRSNmRl4aIdGtLOU_WLCFBekJX8az84tyw/KL4azJlb_mg.jpg?size=687x717&quality=96&sign=a22acdb5886b71e338a3797a4dc39443&type=album', stream=True).raw)
    return im


#Q4
def vpbun_modumo():
    print('''
#Binom
#E(X) = np
#Var(X) = npq

n = 160
p = 0.55

E_X_Y = n * p * p
Var_E_X_Y = E_X_Y * p * (1-p)

print(f"E(X|Y) = {round(E_X_Y,2)}")
print(f"Var(E(X|Y)) = {round(Var_E_X_Y,3)}")
    ''')
    
def vpbun_momoud():
    print('''
n = 79
p = 0.6

E_X_Y = n * p * p
E_Var_X_Y = n * p * (1-p) * p

print(f"E(X|Y) = {round(E_X_Y,2)}")
print(f"E(Var(X|Y)) = {round(E_Var_X_Y,3)}")    
    ''')
    
def vpbun_mouddumo():
    print('''
n = 88
p = 0.7

E_X_Y = n * p * p
Var_X_Y = n * p * (1-p)
E_Var_X_Y = Var_X_Y * p
Var_E_X_Y = E_X_Y * p * (1-p)

print(f"E(Var(X|Y)) = {round(E_Var_X_Y,3)}")
print(f"Var(E(X|Y)) = {round(Var_E_X_Y,3)}")
    ''')
    
def suoop():
    print('''
from scipy.stats import poisson

lambdA = 14/5
E_Xi = 4.4

# Xi ущерб от i-ого пожара
# Y число пожаров за год

E_Y = poisson.mean(lambdA)
Var_Y = poisson.var(lambdA)

Var_X = E_Xi**2

E_S = E_Xi * E_Y
Var_S = (E_Xi**2 * Var_Y) + (Var_X * E_Y)
sigma_S = math.sqrt(Var_S)

print(f'E(S) = {round(E_S,2)}')
print(f'sigma(S) = {round(sigma_S,3)}')
    ''')
    
def muoss():
    print('''
from scipy.stats import poisson
from scipy.stats import uniform

high = 3.3
low = 0
years = 10
cases = 12
lambdA = cases/years

# Xi ущерб от i-ого пожара
# Y число пожаров за год

E_Y = poisson.mean(lambdA)
Var_Y = poisson.var(lambdA)

E_Xi = uniform.mean(loc=low, scale=high)
Var_Xi = uniform.var(loc=low, scale=high)

E_S = E_Y*E_Xi
Var_S = E_Y*Var_Xi + Var_Y*E_Xi**2
sigma_S = math.sqrt(Var_S)

print(f'E(S) = {round(E_S,2)}')

print(f'sigma(S) = {round(sigma_S,3)}')
    ''')
    
def dstsiv():
    print('''
from scipy.stats import randint

dist_range_Y = {2:0.6,15:0.4}
k = 7

dist_range_E_X_Y = {randint.mean(0,i*k+1):j  for i,j in dist_range_Y.items()}

E_XY = sum([i*j*(list(dist_range_Y.keys())[list(dist_range_Y.values()).index(j)]) for i,j in dist_range_E_X_Y.items()])

E_Y = sum([i*j for i,j in dist_range_Y.items()])
E_X = sum([i*j for i,j in dist_range_E_X_Y.items()])

Cov_XY = E_XY - E_X*E_Y

print(f"E_XY = {round(E_XY,2)}")
print(f"Cov_XY = {round(Cov_XY, 3)}")
    ''')
    
def ikimp():
    print('''
from scipy.stats import geom
from scipy.stats import randint

money = 29
n = 8

p_eagle = 1/2
# Y кол-во бросков
# Xi кол-во очков при i броске

p = math.factorial(money) / (math.factorial(money - n) * math.factorial(n)) * p_eagle**money

E_Y = geom.mean(p)
Var_Y = geom.var(p)

E_Xi = randint.mean(low=1, high=7)
Var_Xi = randint.var(low=1, high=7)

E_S = E_Y*E_Xi
Var_S = E_Y*Var_Xi + Var_Y*E_Xi**2
sigma_S = math.sqrt(Var_S)

print('E(S) =', round(E_S, 3))

print('sigma(S) =', round(sigma_S, 3))
    ''')
    
def vgusi():
    print('''
marks = np.array([90, 79, 53, 62, 66, 68, 75, 0, 82, 29, 0, 29, 68, 90, 0, 60, 44, 44, 70, 68, 70, 89, 0, 68, 0, 66, 0, 59, 70])

print(round(marks[marks>0].mean(),1))
M = np.median(marks[marks!=0])
print(round(M))
H = sts.hmean(marks[marks>=M])
print(round(H,1))
G = sts.gmean(marks[marks>=M])
print(round(G,1))
Q = np.median(marks[marks>=M])
print(round(Q))
print(len(marks[(marks >= min(H,Q)) & (marks <= max(H,Q))]))
    ''')
    
def scheun():
    print('''
vals = np.array([-9, 9, -138, -145, 186, 78, 34, -37, -19, -68, -82, 158, 96, -189, 24, 84, -99, 125, -39, 26, 62, -91, 239, -211, 2, 129, 2, -16])

v_mean = vals.mean()
v_std = vals.std()

X = sts.norm(v_mean, v_std)
L = X.ppf(0.25)
H = X.ppf(0.75)

count = len(vals[(vals >= L) & (vals <= H)])

xsort=sorted(vals)
n=len(xsort)

res_d = float('-inf')
for i in range(len(xsort)):
    maxx=max(abs((i+1)/n-X.cdf(xsort[i])),abs((i)/n-X.cdf(xsort[i])))
    if maxx > res_d:
        res_d = maxx
        d_ind = i
        
distation = res_d

print('Среднее арифметическое ПД =', v_mean)
print('Эмпирическое стандартное отклонение ПД =', v_std)
print('Квартиль L =', L)
print('квартиль Н =', H)
print('Количество ПД, попавших в интервал от L до H = \', count)
print('Расстояние между функциями распределений =', distation)
    ''')
    
def vgusp_kkk():
    print('''
import re
#переместить в тройные кавычки
s = 'x1=71,y1=71
, x2=52,y2=58
, x3=72,y3=81
, x4=87,y4=92
, x5=81,y5=81
, x6=100,y6=94
, x7=90,y7=96
, x8=54,y8=46
, x9=54,y9=60
, x10=58,y10=62
, x11=56,y11=49
, x12=70,y12=60
, x13=93,y13=86
, x14=46,y14=48
, x15=56,y15=61
, x16=59,y16=52
, x17=42,y17=40
, x18=60,y18=60
, x19=33,y19=37
, x20=83,y20=92
, x21=50,y21=57
, x22=93,y22=93
, x23=41,y23=42
, x24=55,y24=64
, x25=60,y25=59
, x26=37,y26=30
, x27=71,y27=71
, x28=42,y28=44
, x29=85,y29=82
, x30=39,y30=39'

match = re.findall(r'=(\d+)', s)
x_all = list(map(int, match[::2]))
y_all = list(map(int, match[1::2]))

x = []
y = []

for x_t, y_t in zip(x_all, y_all):
    if x_t >= 50 and y_t >= 50:
        x.append(x_t)
        y.append(y_t)
        
x = np.array(x)
y = np.array(y)

cov = 0
for x_t, y_t in zip(x, y):
    cov += (x_t - x.mean()) * (y_t - y.mean())
cov /= len(x)

corr = cov/np.sqrt(x.var()*y.var())

print('Ковариация = ', cov)
print('Коэффициент корреляции = ', corr)
    ''')
    
def psign():
    print('''
k = 3
n = [24, 26, 30]
xi = [70, 76, 77]
sigma = [4, 6, 8]

N = sum(n)

l_1 = []
for i in range(k):
    l_1.append(n[i]*xi[i])
x = 1/N *sum(l_1)
print("Среднее значение:", round(x,3))

l_2 = []
for i in range(k):   
    l_2.append(n[i]*(xi[i]-x)**2)

l_3 = []
for i in range(k):
    l_3.append(sigma[i]**2*n[i])

standart_otkl = (1/N * (sum(l_2) + sum(l_3)))**0.5
print("Стандартное отклонение:", round(standart_otkl, 4))
    ''')
    
def vgusp_dtsm():
    print('''
# Оценки в группе
X_group = [100, 86, 51, 100, 95, 100, 12, 61, 0, 0, 12, 86, 0, 52, 62, 76, 91, 91, 62, 91, 65, 91, 9, 83, 67, 58, 56]

# Количество выборок
n_samples = 7

# 1) Дисперсия Var(X¯¯¯¯)
var_X_bar = np.var(X_group) / n_samples

mean_X_group = np.mean(X_group)
moment_3 = np.mean((X_group - mean_X_group) ** 3)/n_samples**2

#centr_mom_x_sr = (np.mean(X_group**3) - 3*np.mean(X_group)*np.mean(X_group**2) + 2*np.mean(X_group)**3)/n**2

print("1) Дисперсия Var(X¯¯¯¯):", round(var_X_bar, 3))
print("2) Центральный момент μ3(X¯¯¯¯):", round(moment_3, 3))
    ''')
    
def vgusp_mod():
    print('''
N = 27 #количество студентов в группе, объем генеральной совокупности
n = 6  #количество выбранных студентов, обхем выборочной совокупности
#бесповторная выборка 

marks = np.array([100, 78, 77, 51, 82, 100, 73, 53, 78, 55, 7, 0, 81, 15, 96, 12, 71, 70, 53, 0, 73, 100, 55, 100, 59, 89, 81]) #оценки в группе

E_x_sr = np.mean(marks)
Var_x_sr = (np.var(marks)/n) * ((N - n)/(N - 1))

print('Математическое ожидание =',round(E_x_sr,3))
print('Дисперсия =',round(Var_x_sr,3))
    ''')
    
def rbned():
    print('''
marks = np.array([2,3,4,5]) #оценка работы
count_works = np.array([7, 48, 8, 105])  #количество работ
teachers = 6
N = np.sum(count_works)   # объем генеральной совокупности
n = N/teachers   # объем выборочной совокупности


mean_mean_x = (count_works@marks)/N
var_mean_x = ((marks**2@count_works)/N - ((count_works@marks)/N)**2) * ((N-n)/(n*(N-1)))

print('Математическое ожидание =',round(mean_mean_x,2))
print('стандартное отклонение =',round(np.sqrt(var_mean_x),3))
    ''')
    
def dikki():
    print('''
n = 19 # количество различных комбинаций 
a = 11 #коэффициент перед R в случайной велечине X
b = -9  #коэффициент перед B в случайной велечине X

red = [1, 2, 3, 4, 5, 6]
blue = [1, 2, 3, 4, 5, 6]

E_r = np.mean(red)
var_r = np.var(red)
E_b = np.mean(blue)
var_b = np.var(blue)

N = 36

mean_mean_x = a*E_r + b*E_b
var_mean_x = (a**2*var_r + b**2*var_b)*(((N-n)/(n*(N-1))))

print('Математическое ожидание =',round(mean_mean_x,2))
print('стандартное отклонение =',round(np.sqrt(var_mean_x),3))
    ''')
    
def ipmmp():
    print('''
n = 11 # количество пронумеронованных монет в броске
m = 257 # количество различных комбинаций орел-решка

#количество орлов в броске распределено по биноминальному закону ==> E(X) = np
p=1/2
N = 2**n # количество различных вариантов бросков --> генереальная совокпность 

mean_mean_x = n*p
var_mean_x = (n*p*(1-p)) * (((N - m)/( m*(N-1))))

print('Математическое ожидание =',round(mean_mean_x,2))
print('стандартное отклонение =',round(var_mean_x,3))
    ''')
    
def erpin_modkk():
    print('''
N = 100 #генеральная совокупность 
n = 7 #бесповторная вбыорка
X = np.array([100,400]) 
Y = np.array([1,2,3])
XY = np.array([[11,32,11],[24,11,11]])


X_n = np.array([np.sum(row) for row in XY])
Y_n = np.array([np.sum(row) for row in np.transpose(XY)])

x_mean = X_n@X/np.sum(X_n)
y_mean = Y_n@Y/np.sum(Y_n)

var_x_mean = ((X**2@X_n)/np.sum(X_n) - (X_n@X/np.sum(X_n))**2 ) * (((N-n)/(n*(N-1))))
var_y_mean = ((Y**2@Y_n)/np.sum(Y_n) - (Y_n@Y/np.sum(Y_n))**2 ) * (((N-n)/(n*(N-1))))

cov_x_y = np.sum([(X[i] - x_mean)*np.sum([(Y[j] - y_mean) * XY[i][j] for j in range(len(Y))]) for i in range(len(X)) ])/N * (((N-n)/(n*(N-1))))

p = cov_x_y  / np.sqrt((var_x_mean*var_y_mean))

print('математическое ожидание X_mean =',round(x_mean,3))
print('дисперсия Y_mean =',round(var_y_mean,3))
print('коэффициент корреляции =',round(p,3))
    ''')
    
def erpin_mosok():
    print('''
N = 100 #генеральная совокупность 
n = 6 #бесповторная вбыорка
X = np.array([100,300]) 
Y = np.array([1,2,4])
XY = np.array([[21,17,12],[10,27,13]])


X_n = np.array([np.sum(row) for row in XY])
Y_n = np.array([np.sum(row) for row in np.transpose(XY)])

x_mean = X_n@X/np.sum(X_n)
y_mean = Y_n@Y/np.sum(Y_n)

var_x_mean = ((X**2@X_n)/np.sum(X_n) - (X_n@X/np.sum(X_n))**2 ) * (((N-n)/(n*(N-1))))
var_y_mean = ((Y**2@Y_n)/np.sum(Y_n) - (Y_n@Y/np.sum(Y_n))**2 ) * (((N-n)/(n*(N-1))))

cov_x_y = np.sum([(X[i] - x_mean)*np.sum([(Y[j] - y_mean) * XY[i][j] for j in range(len(Y))]) for i in range(len(X)) ])/N * (((N-n)/(n*(N-1))))


print('математическое ожидание X_mean =',round(y_mean,4))
print('дисперсия Y_mean =',round(np.sqrt(var_x_mean),3))
print('ковариация=',round(cov_x_y,3))
    ''')
    
def iielp():
    print('''
import scipy.integrate as integrate
sample = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 0, 3, 2, 2, 5, 0, 6, 1, 6, 4, 4, 7, 7, 13, 7, 12, 22, 15, 20, 27, 21, 28, 30, 25, 37, 42, 42, 30, 39, 45, 54, 57, 48, 61, 46, 42, 45, 37, 29, 22, 22, 8, 10, 5, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0])
percents = []
for i in range(len(sample)):
    if sample[i] != 0:
        l = [i]*sample[i]
        percents.extend(l)
percents = np.array(percents)/100
def lnL(X, a, b):
    n = X.shape[0]
    return n*np.log(a) + n*np.log(b) + (a-1)*np.sum(np.log(X)) + (b-1)*np.sum(np.log(1-X**a))
maxL = -np.inf
for a in range(1, 21):
    for b in range(1, 21):
        L = lnL(percents, a, b)
        if L > maxL:
            maxL = L
            a_max = a
            b_max = b
        
print('A',a_max, 'B',b_max)
a, b = a_max, b_max
def f_x(x):
    return a*b*x**(a-1)*(1 - x**a)**(b-1)

def xfx(x):
    return x*f_x(x)

result = integrate.quad(xfx, 0, 1)[0]
print('Математическое ожидание',result)

def F(x):
    return integrate.quad(f_x, 0, x)[0]

x_val = np.linspace(0, 1, 1000000)
q = 0.2
for x in x_val:
    if F(x) >= q:
        print('Квантиль', x)
        break
    ''')
    
def prsvid():
    print('''
x = '-0,616; -0,238; 0,173; -0,255; 0,531; 0,718; -0,161; 0,371; -1,014; -0,413; -1,571; 0,485; 0,486; 0,688; -0,944; 0,155; 0,003; 0,111; 0,752; 0,783; -0,102; -0,74; -2,097; 1,349; -0,044; -0,617; -0,782; -0,873; -0,995; -1,256; -0,596'
x = np.array(list(map(float, (x.replace(',', '.').replace(';', ',')).split(','))))

y = '-1,34; -0,25; 0,101; -0,626; -0,088; 0,539; -0,451; 0,233; -1,186; -0,423; -1,329; 0,231; 0,209; 0,638; -0,274; -0,491; -0,319; 0,294; 0,895; 1,164; -0,57; -1,078; -1,526; 1,491; 0,182; -0,31; -1,001; -0,969; -0,918; -0,904; -0,595'
y = np.array(list(map(float, (y.replace(',', '.').replace(';', ',')).split(','))))

rho_ = np.corrcoef(x, y)[0][1]
n = len(x)
gamma = 0.93
z = sts.norm.ppf((1+gamma)/2)
delta = (1/((n-3)**0.5))*z
z_n = math.atanh(rho_)
theta_1 = math.tanh(math.atanh(rho_) - delta)
theta_2 = math.tanh(math.atanh(rho_) + delta)

print(f' Rho = {round(rho_, 3)}\n Theta_2 = {round(theta_2, 3)}')
    ''')
    
def prsvin_z():
    print('''
x = '1,416; 0,624; 6,471; 6,256; 1,787; 2,546; -1,758; -5,475; 0,077; 1,792; 5,443; 5,348; -0,057; 0,232; -2,305; -3,568; -4,541; 7,893; -0,473; -0,229; -3,0; 3,903; -4,227; 0,537; -1,785; 2,575; -0,477; -2,754; 1,164; 2,716'
x = np.array(list(map(float, (x.replace(',', '.').replace(';', ',')).split(','))))
mu0 = 1.29
sigma = 3.4
alpha = 0.01
mu1 = 1.17

n = len(x)
x_ = x.mean()

Z = (x_ - mu0)/(sigma/(n**0.5))
A_cr = sts.norm.isf(alpha/2)
P = 2*min(sts.norm.sf(Z), 1-sts.norm.sf(Z))

z_alpha_2 = sts.norm.isf(alpha/2)
W = 1 - (sts.norm.cdf(z_alpha_2 - ((n**0.5)/sigma) * (mu1 - mu0)) - 1/2 + sts.norm.cdf(z_alpha_2 + ((n**0.5)/sigma) * (mu1 - mu0)) - 1/2)
print(f'1) Значение статистики критерия Zнабл. = {round(Z,3)}')
print(f'2) Граница А критического множества = {round(A_cr,3)}')
print(f'3) P-значение критерия = {round(P,3)}')
print(f'4) Мощность W критерия = {round(W,3)}')
    ''')
    
def prsvin_t():
    print('''
x = '1,146; 2,958; -3,325; -0,534; 0,374; 5,293; 0,12; 1,185; 5,148; 5,351; 2,639; 1,47; -1,967; 4,96; 6,057; -0,542; 1,544; -0,243; -1,988; 2,844'
x = np.array(list(map(float, (x.replace(',', '.').replace(';', ',')).split(','))))
alpha = 0.05
mu0 = 1.1
mu1 = 0.91

n = len(x)
x_sr = np.mean(x)
s_ = np.std(x,ddof=1)
se = s_/n**0.5

t_obs=(x_sr-mu0)/se
t_cr = sts.t.isf(alpha/2, n-1)

p_val = 2*min(sts.t.sf(t_obs,n-1),sts.t.cdf(t_obs,n-1))

delta = np.sqrt(n)*(mu1-mu0)/s_
w = 1 - (sts.nct.cdf(t_cr, n-1, delta) - sts.nct.cdf(-t_cr, n-1, delta))

print(f'1) Значение статистики критерия t=Tнабл = {round(t_obs,3)}')
print(f'2) Граница А критического множества = {round(t_cr,3)}')
print(f'3) P-значение критерия = {round(p_val,3)}')
print(f'4) Мощность W критерия = {round(w,3)}')
    ''')
    
def prsvin_chi20():
    print('''
x = '0,889; 1,514; 2,846; 2,811; 0,84; 0,945; 0,02; -0,441; -0,796; 3,739; 0,688; 0,777; -0,233; 2,284; -0,681; 1,056; 0,21; 1,8; 0,687; -0,144; 1,285; 1,851; 1,402; 1,695; 0,533; 0,87; 0,486; 0,874; 0,312; -0,821'
x = np.array(list(map(float,x.replace(',','.').split(';'))))
mu = 1.18
alpha = 0.02
sigma_0 = 1.14
sigma_1 = 1.24

chi2_obs = sum((x-mu)**2)/sigma_0**2

A = sts.chi2.ppf(alpha/2,len(x))
B = sts.chi2.isf(alpha/2,len(x))

pv1 = sts.chi2.cdf(chi2_obs,len(x))
pv2 = 1 - pv1
p_val = 2*min(pv1,pv2)

beta = sts.chi2.cdf(sigma_0**2/sigma_1**2*B,len(x)) - sts.chi2.cdf(sigma_0**2/sigma_1**2*A,len(x))

print(f'1) Значение статистики критерия χ2 = {round(chi2_obs,3)}')
print(f'2) Границы А и В критического множества = {round(A,3)}; {round(B,3)}')
print(f'3) P-значение критерия = {round(p_val,3)}')
print(f'4) Вероятность ошибки второго рода β = {round(beta,3)}')
    ''')
    
def prsvin_chi2():
    print('''
x = '0,889; 1,514; 2,846; 2,811; 0,84; 0,945; 0,02; -0,441; -0,796; 3,739; 0,688; 0,777; -0,233; 2,284; -0,681; 1,056; 0,21; 1,8; 0,687; -0,144; 1,285; 1,851; 1,402; 1,695; 0,533; 0,87; 0,486; 0,874; 0,312; -0,821'
x = np.array(list(map(float,x.replace(',','.').split(';'))))
alpha = 0.02
sigma_0 = 1.14
sigma_1 = 1.24

x_sr = np.mean(x)
chi2_obs = sum((x-x_sr)**2)/sigma_0**2

A = sts.chi2.ppf(alpha/2,len(x)-1)
B = sts.chi2.isf(alpha/2,len(x)-1)

pv1 = sts.chi2.cdf(chi2_obs,len(x)-1)
pv2 = 1 - pv1
p_val = 2*min(pv1,pv2)

beta = sts.chi2.cdf(sigma_0**2/sigma_1**2*B,len(x)-1) - sts.chi2.cdf(sigma_0**2/sigma_1**2*A,len(x)-1)

print(f'1) Значение статистики критерия χ2 = {round(chi2_obs,3)}')
print(f'2) Границы А и В критического множества = {round(A,3)}; {round(B,3)}')
print(f'3) P-значение критерия = {round(p_val,3)}')
print(f'4) Вероятность ошибки второго рода β = {round(beta,3)}')
    ''')
    
def prsvin_xy_z():
    print('''
x = '3,842; 3,374; 4,18; 4,5; 4,247; 4,412; 3,756; 3,946; 3,729; 3,948; 3,631; 2,992; 4,324; 3,919; 3,059; 4,524; 3,565; 4,236; 4,71; 4,29; 4,998; 3,336; 4,482; 3,721; 3,59'
X = np.array(list(map(float, (x.replace(',', '.').replace(';', ',')).split(','))))
y = '3,19; 3,564; 4,079; 2,369; 5,261; 4,652; 1,849; 6,084; 6,654; 5,65; 3,748; 2,501; 5,476; 3,436; 5,711; 4,292; 5,367; 4,499; 4,989; 4,015; 6,5; 4,178; 4,563; 6,636; 2,113; 2,221; 5,357; 2,358; 6,721; 3,421'
Y = np.array(list(map(float, (y.replace(',', '.').replace(';', ',')).split(','))))
sigma_x = 0.7
sigma_y = 1.4
alpha = 0.02
delta = 0.1

n = len(X)
m = len(Y)
X_mean = X.mean()
Y_mean = Y.mean()
Z_obs = (X_mean - Y_mean) / (np.sqrt((sigma_x**2 / n) + (sigma_y**2 / m)))

p_val = sts.norm.sf(Z_obs)

A = sts.norm.isf(alpha)

beta = sts.norm.cdf(A - np.sqrt((n * m) /(m * sigma_x**2 + n * sigma_y**2)) * delta)
W = 1 - beta

print(f'1) Значение статистики критерия Zнабл = {round(Z_obs,3)}')
print(f'2) P-значение критерия = {round(p_val,3)}')
print(f'3) Граница А критического множества = {round(A,3)}')
print(f'4) Мощность W критерия = {round(W,3)}')
    ''')
    
def dtgfp():
    print('''
A = '0,616; 1,046; 2,575; -0,344; 2,339; -0,68; 3,739; 2,251; -1,252; 3,536; -0,491; 5,556; 4,856; -1,68; 2,33; 1,345; 2,829; 2,539; 3,304; 3,497; 0,211; 3,563; 0,94; 3,642; 1,956; 3,919; 3,568'
B = '2,834; 1,504; -0,678; 5,619; 0,97; 1,617; 3,768; -1,309; 3,343; -1,778; -0,854; 1,04; 2,83; -2,335; 4,853; 5,6; 4,341; 4,362; 3,52; 1,151; -0,621; -2,88; 1,697; 1,753; 0,211; 2,157; 1,989; 2,457; 1,399; 1,61; -0,558; 2,132; 2,293'
C = '2,398; -2,77; 4,679; 1,924; 0,574; 5,329; 0,699; 4,457; -0,3; 1,682; -1,34; 0,046; -1,096; 1,935; 2,411; 4,134; 5,643; 3,071; 6,526; 4,941; 2,844; -0,43; -2,066; 0,22; 0,317; -1,923; 1,38; -2,485; 0,111; -0,542; 4,78; 1,93; 0,462; 5,487; -3,547; 2,933; -0,987; -0,21; 3,955'
A = np.array(list(map(float, (A.replace(',', '.').replace(';', ',')).split(','))))
B = np.array(list(map(float, (B.replace(',', '.').replace(';', ',')).split(','))))
C = np.array(list(map(float, (C.replace(',', '.').replace(';', ',')).split(','))))
alpha = 0.03
                  
n_A = len(A)
n_B = len(B)
n_C = len(C)
n_list = [n_A, n_B, n_C]
n = sum(n_list)
GROUPS = [A,B,C]

mean_group_var = sum([np.sum((G-G.mean())**2) for G in GROUPS])/n
X_vyb_mean = np.dot([G.mean() for G in GROUPS], n_list)/n
among_groups_var = np.dot(([G.mean() for G in GROUPS] - X_vyb_mean)**2, n_list)/n

k = len(GROUPS)
MSW = (mean_group_var * n) / (n - 3)            
MSA = (among_groups_var * n) / (k - 1)
F_obs = MSA / MSW


p_val = sts.f.sf(F_obs, k - 1, n - k)

print(f'1) Межгрупповая дисперсия = {round(among_groups_var,3)}')
print(f'2) Средняя групповая дисперсия = {round(mean_group_var,3)}')
print(f'3) Значение статистики критерия = {round(F_obs, 3)}')
print(f'4)P-значение критерия = {round(p_val, 3)}')
    ''')
    
def dtgfp_file():
    print('''
data = pd.read_csv('ds5.9.8.csv', delimiter=';', header=None)
gamma = 0.91
alpha = 0.03

A = np.array([float(str(i).replace(',', '.')) for i in data.loc[:,0].dropna()])
B = np.array([float(str(i).replace(',', '.')) for i in data.loc[:,1].dropna()])
C = np.array([float(str(i).replace(',', '.')) for i in data.loc[:,2].dropna()])

n_A = len(A)
n_B = len(B)
n_C = len(C)
n_list = [n_A, n_B, n_C]
n = sum(n_list)
GROUPS = [A,B,C]

mean_group_var = sum([np.sum((G-G.mean())**2) for G in GROUPS])/n
X_vyb_mean = np.dot([G.mean() for G in GROUPS], n_list)/n
among_groups_var = np.dot(([G.mean() for G in GROUPS] - X_vyb_mean)**2, n_list)/n

k = len(GROUPS)
MSW = (mean_group_var * n) / (n - 3) #остаточная дисперсия

deltas = [np.sqrt(MSW / n_) * sts.t.ppf((1 + gamma) / 2, n - k) for n_ in n_list]

MSA = (among_groups_var * n) / (k - 1) #факторная дисперсия
F_obs = MSA / MSW

F_alpha = sts.f.isf(alpha, k - 1, n - k)
#1
print(f'Межгрупповая дисперсия = {round(among_groups_var,6)}')
print(f'Средняя групповая дисперсия = {round(mean_group_var,5)}')
#2
for G, delta in zip(GROUPS, deltas):
    print(f'mu{deltas.index(delta)+1} in ({round(G.mean() - delta, 6)}; {round(G.mean() + delta, 6)})')
#3    
print(f'Fнабл = {round(F_obs, 5)}')
print(f'Fкр = {round(F_alpha, 5)}')
print(f'K_alpha = ({round(F_alpha, 5)} < {math.inf})')
print('H0 отвергаем') if (F_obs > F_alpha) else print('H0 не отвергаем')
#4
p_val = sts.f.sf(F_obs, k - 1, n - k)
print(f'p_val = {round(p_val, 6)}')
print('H0 отвергаем') if (p_val < alpha) else print('H0 не отвергаем')
    ''')
    
def psvfr():
    print('''
data = pd.read_csv('ds6.4.12.csv', delimiter=';', header=None)
mX = 2
mY = 2

X = np.array([float(str(i).replace(',', '.')) for i in data.loc[:,0].dropna()])
Y = np.array([float(str(i).replace(',', '.')) for i in data.loc[:,1].dropna()])

sigma, rho, pi = sp.symbols('sigma, rho, pi')

E_X = X.mean()
E_Y = Y.mean()
n = len(X)

A = np.sum((X - mX)**2) / n
B = np.sum((Y - mY)**2) / n
C = np.sum((X - mX) * (Y - mY)) / n

f = 1 / (2*pi*sigma**2*(1 - rho**2)**0.5) * sp.exp((-1 / (2*(1-rho**2)*sigma**2)) * (A - 2*rho*C + B))
ln_L = -sp.ln(2*pi) - 2*sp.ln(sigma) - 1/2*sp.ln(1-rho**2) - (A-2*rho*C + B)/(2*(1-rho**2)*sigma**2)

diff_ln_L_sigma = sp.diff(ln_L, sigma)
diff_ln_L_rho = sp.diff(ln_L, rho)

solves = sp.solve([diff_ln_L_sigma, diff_ln_L_rho],[rho, sigma])

print('Логарифм:', ln_L)
#нужное решение выбрать исходя из ограничений
print('Решения (rho, sigma):', solves)
''')
    
    


def help_libraries():
    print('''
import numpy as np
import math
import scipy.stats as sts
import pandas as pd
import sympy as sp
from scipy.stats import geom
from scipy.stats import randint
from scipy.stats import uniform
from scipy.stats import poisson
from scipy.stats import expon
from scipy.stats import binom
import matplotlib.pyplot as plt

sp.init_printing()''')
    
def help_q1():
    print('''
    Q1
    dosvkig() 
    1. Дайте определение случайной величины, которая имеет гамма-распределение Γ(α, λ),  и выведите основные свойства гамма-расределения.  Запишите формулы для математичсекого ожидания E(X) и дисперсии Var(X) гамма-распределения.
    
    dosvkichi2()
    2. Дайте определение случайной величины, которая имеет χ2-распределение с n степенями свободы. Запишите плотность χ2- распределения. Выведите формулы для математического ожидания E(X)и дисперсии Var(X) χ2-распределение с n степенями свободы. Найдите а) P(χ2,20 > 10.9), где χ2,20 – случайная величина, которая имеет χ2– распределение с 20 степенями свободы; б) найдите 93% (верхнюю) точку χ2,0.93(5) хи-квадрат распределения с 5 степенями свободы. Ответ: P(χ2,20 > 10.9) = 0.948775; χ2,0.93(5) = 1.34721.
    
    dosvkirs()
    3. Дайте определение случайной величины, которая имеет распределение Стьюдента с n степенями свободы Как связаны распределение Коши и распределение Стьюдента? Запишите плотность распределения Стьюдента с четырьмя степенями свободы. Найдите а) P(−2.5 =< t5 < −1.7), где t5 – случайная величина, которая имеет распределение Стьюдента с 5 степенями свободы; б) найдите 10% (верхнюю) точку t0.1(7) распределения Стьюдента 7 степенями свободы. Ответ: а) P(−2.5 =< t5 < −1.7) = 0.0476933; t0.1(7) = 1.41492
    
    dosvkirf()
    4. Дайте определение случайной величины, которая имеет распределение Фишера F(n, m) с n и m
    степенями свободы. Запишите плотность распределения Фишера F(n, m) с n и m степенями свободы. 
    Какой закон распределения имеет случайная величина 1/F, если случайная величина F имеет
    распределение Фишера F(n, m) с n и m степенями свободы? Ответ необходимо обосновать. 
    Найдите а) P(3.1 <= 1/F < 10.7), где F – случайная величина, которая имеет распределение Фишера с 3 и 5
    степенями свободы, F ∼ F(3; 5); б) найдите 5% (верхнюю) точку F0.05(13; 4) распределения Фишера
    с 13 и 4 степенями свободы.

    dopti()
    5. Дайте определения процентной точки и квантили. Укажите связь между процентными точками и
    квантилями. Сформулируте основные свойтсва процентных точек. 
    Выведите формулу для нахождения процентной точки стандартного нормального 
    закона распределения через функцию Лапласа Φ0(x). Найдите P(0.3 < Z2 < 3.7), 
    если случайная величина Z имеет стандартное нормальноераспределение, Z ∼ N(0; 1).

    sosvik()
    6. Сформулируйте определение случайной выборки из конечной генеральной совокупности. Какие
    виды выборок вам известны? Перечислите (с указанием формул) основные характеристики 
    выборочной и генеральной совокупностей

    sosvir()
    7. Сформулируйте определение случайной выборки из распределения. Как в этом случае определяются: 
    выборочное среднее, начальные и центральные моменты выборки, функция распределения
    выборки? Что в данном контексте означает генеральное среднее?

    zfdmo()
    8. Запишите формулы для математического ожидания и дисперсии выборочной доли в случае повторной 
    (бесповторной) выборки. Поясните все используемые обозначения.

    sovfr()
    9. Сформулируйте определение выборочной функции распределения и докажите ее сходимость по
    вероятности к теоретической функции распределения. Выведите формулы для математического
    ожидания и дисперсии выборочной функции распределния.

    dokps()
    10. Дайте определение k-ой порядковой статистики. Выведение формулы для функций
    распределений экстремальных статистик.

    chttso()
    11. Что такое точечная статистическая оценка? Какие оценки называются несмещенными, состоятельными? 
    Приведите пример оценки с минимальной дисперсией.

    siddu()
    12. Сформулируйте и докажите достаточное условие состоятельности оценки.

    sosoo()
    13. Сформулируйте определение среднеквадратичной ошибки оценки. Какая оценка называется 
    оптимальной? В чем заключается среднеквадратический подход к сравнению оценок?

    skooo()
    14. Сформулируйте критерий оптимальности оценки, основанной на неравенстве Рао-Крамера.

    doipfi()
    15. Дайте определение информации по Фишеру и сформулируйте информационное неравенство РаоКрамера.

    soeoprkn()
    16. Сформулируйте определение эффективной оценки по Рао-Крамеру. Найдите эффективную оценку 
    параметра θ для распределения Бернулли Bin(1, θ).

    dnsie()
    17. Докажите несмещенность, состоятельность и эффективность 
    (в классе всех линейных несмещенных оценок) выборочного среднего X.

    soeoprkd()
    18. Сформулируйте определение эффективной оценки по Рао–Крамеру. Для 
    распределения Пуассона Π(λ) предлагается оценка параметра λ:  λ̂ =𝑋¯. 
    Покажите, что эта оценка является эффективной по Рао-Крамеру.

    sinrk()
    19. Сформулируйте информационное неравенство Рао–Крамера. Исследуйте на 
    эффективность оценку p_hat = X_sr/m
    для биномиального распределения Bin(m; p).

    doipfv()
    20. Дайте определение информации по Фишеру. Вычислите информацию Фишера для нормального
    закона распределения N(µ; σ2) (дисперсия σ2 известна) и проверьте, 
    что выборочное среднее X является эффективной оценкой параметра µ = E(X).

    kpopa()
    21. Как производится оценка параметров абсолютно непрерывного 
    распределения методом максимального правдоподобия? Какой вероятностный 
    смысл в этом случае имеет функция правдоподобия? Найдите методом максимального 
    правдоподобия оценку параметра θ равномерного распределения U([θ; θ + 5]).

    kpopr()
    22. Как производится оценка параметров распределения методом моментов? 
    Найдите методом моментов оценку параметра θ равномерного распределения U([−θ; θ].

    sodop()
    23. Сформулируйте определение доверительной оценки параметра с коэффициентом доверия γ. 
    Какой интервал называется асимптотически доверительным. Что такое точность доверительной оценки?
    
    pfsvd_var_i()
    24. Приведите формулы (с выводом) доверительного точного интервала для параметра сдвига θ = µ
    нормальной модели N(µ; σ2), когда параметр масштаба σ2 известен. Является ли такой интервал
    симметричным по вероятности? Ответ обосновать.
    
    pfsvd_mu_i()
    25. Приведите формулы (с выводом) доверительного точного интервала для параметра масштаба θ =σ2 нормальной модели N(µ; θ), когда значение параметра сдвига µ известно. Является ли такой
    интервал симметричным по вероятности? Ответ обосновать.

    pfsvd_var_n()
    26. Приведите формулы (с выводом) доверительного точного интервала для параметра сдвига θ = µ
    нормальной модели N(µ; σ2), когда параметр масштаба σ2– неизвестен. Является ли такой интервал симметричным по вероятности? Ответ обосновать.
    
    pfsvd_mu_n()
    27. Приведите формулы (с выводом) доверительного точного интервала для параметра масштаба θ =σ2 нормальной модели N(µ; θ), когда параметр сдвига µ – неизвестен. Является ли такой интервал
    симметричным по вероятности? Ответ обосновать.
    
    stfpv()
    28. Сформулируйте теорему Фишера. Пусть X1, X2, . . . Xn – выборка объема n из N(µ; σ2). Найдите а)
    Cov(Xi − X; X); б) Cov(Xi − X; Xj − X), i 6= j
    
    pfsvd_pred()
    29. Приведите формулы (с выводом) доверительного точного интервала предсказания для Xn+1 по выборке X1, X2, . . . , Xn из нормальной модели N(µ; σ2), когда оба параметр µ и σ2– неизвестны. Является ли такой интервал симметричным по вероятности? Ответ обосновать.
    
    doadi_rho()
    30. Дайте определение асимптотического доверительного интервала и приведите формулы (с выводом) асимптотического доверительного интервала для коэффициента корреляции ρ по выборке
    (X1; Y1),(X2; Y2), . . .(Xn; Yn) объема n из двумерной нормальной модели N(µ1; µ2; σ21; σ22; ρ). Является ли такой интервал симметричным по вероятности? Ответ обосновать.
    
    doadi_prob()
    31. Дайте определение асимптотического доверительного интервала и приведите формулы (с выводом) асимптотического доверительного интервала для парамера вероятности θ = p. Выведите
    уравнение доверительного эллипса.
    
    pvoig_ost_var()
    32. Пусть X~j = (X1j , X2j , . . . , Xnj j ) – выборка объема nj из N(µj ; σ2), где j = 1, . . . , k. Приведите формулы (с выводом) доверительного интервала для параметра µj , используя в качестве несмещеннойоценки параметра σ2 остаточную дисперсию 1n−kPkj=1Pnji=1Xij − Xj2. Является ли такой интервал
    симметричным по вероятности? Ответ обосновать
    
    pvoig_var_tozhd()
    33.  Пусть X~j = (X1j , X2j , . . . , Xnj j ) – выборка объема nj из N(µj ; σ2), где j = 1, . . . , k. Приведите формулы (с выводом и необходимыми пояснениями в обозначениях) дисперсионного тождества.
    
    pvoig_fact_var()
    34.  Пусть X~j = (X1j , X2j , . . . , Xnj j ) – выборка объема nj из N(µj ; σ2), где j = 1, . . . , k. Дайте определениефакторной дисперсии. Приведите формулу (с выводом и необходимыми пояснениями в обозначениях) математического ожидания факторной дисперсии
''')    
    
def help_q2():
    print('''
    Q2
    oosps()
    1. Опишите общую схему проверки статистических гипотез. Определите понятия: критическая область, уровень значимости, мощность критерия. Какие гипотезы называются простыми (сложными)
    
    pviop()
    2. Приведите вероятностную интерпретацию ошибок первого и второго рода, а также мощности критерия в случае простых нулевой и альтернативной гипотез. Привести пример критерия с выбором
    критического значения c0, для которого сумма ошибок первого и второго рода α + β была бы минимальной
    
    donis()
    3. Дайте определение несмещенности и состоятельности критерия. Пусть мощность критерия определяется выражением W(µ) = 12 − Φ0zα −√nσ(µ − µ0, µ ∈ Θ1 = (µ0; +∞). Является ли критерий с
    такой функцией мощности несмещенным и состоятельным? Ответ обосновать
    
    slnpv()
    4. Сформулируйте лемму Неймана-Пирсона в случае проверки двух простых гипотез. Приведите
    пример построения наиболее мощного критерия.
    
    pvoin_var_izv_mu_b()
    5. По выборке X1, X2, . . . , Xn объема n из нормального закона распределения N(µ; σ2), когда σ2 =
    Var(X) – известна, проверяется на уровне значимости α основная гипотеза H0 : µ = µ0 против 
    альтернативной гипотезы H1 : µ > µ0. 1) Приведите необходимую статистику критерия и критическое множество для проверки H0 против H1. 
    2) Приведите (с доказательством) основные свойства
    критерия. 3) Приведите (с выводом) выражение для P-значения критерия

    pvoin_var_izv_mu_m()
    6. По выборке X1, X2, . . . , Xn объема n из нормального закона распределения N(µ; σ2), когда σ2 =
    Var(X) – известна, проверяется на уровне значимости α основная гипотеза H0 : µ = µ0 против 
    альтернативной гипотезы H1 : µ < µ0. 1) Приведите необходимую статистику критерия и критическое 
    множество для проверки H0 против H1. 2) Приведите (с доказательством) основные свойства
    критерия. 3) Приведите (с выводом) выражение для P-значения критерия

    pvoin_var_izv_mu_n()
    7. По выборке X1, X2, . . . , Xn объема n из нормального закона распределения N(µ; σ2), 
    когда σ2 = Var(X) – известна, проверяется на уровне значимости α основная гипотеза H0 : µ = µ0 
    против альтернативной гипотезы H1 : µ ≠ µ0. 1) Приведите необходимую статистику критерия и критическое 
    множество для проверки H0 против H1. 2) Приведите (с доказательством) основные свойства
    критерия. 3) Приведите (с выводом) выражение для P-значения критерия

    pvoin_var_neizv_mu_b()
    8. По выборке X1, X2, . . . , Xn объема n из нормального закона распределения N(µ; σ2), когда σ2 =
    Var(X) – неизвестна, проверяется на уровне значимости α основная гипотеза H0 : µ = µ0 против
    альтернативной гипотезы H1 : µ > µ0. 1) Приведите необходимую статистику критерия и критическое 
    множество для проверки H0 против H1. 2) Приведите (с доказательством) основные свойства
    критерия. 3) Приведите (с выводом) выражение для P-значения критерия.

    pvoin_var_neizv_mu_m()
    9. По выборке X1, X2, . . . , Xn объема n из нормального закона распределения N(µ; σ2), когда σ2 =
    Var(X) – неизвестна, проверяется на уровне значимости α основная гипотеза H0 : µ = µ0 против
    альтернативной гипотезы H1 : µ < µ0. 1) Приведите необходимую статистику критерия и критическое 
    множество для проверки H0 против H1. 2) Приведите (с доказательством) основные свойства
    критерия. 3) Приведите (с выводом) выражение для P-значения критерия.

    pvoin_var_neizv_mu_n()
    10. По выборке X1, X2, . . . , Xn объема n из нормального закона распределения N(µ; σ2), когда σ2 =
    Var(X) – неизвестна, проверяется на уровне значимости α основная гипотеза H0 : µ = µ0 против
    альтернативной гипотезы H1 : µ ≠ µ0. 1) Приведите необходимую статистику критерия и критическое 
    множество для проверки H0 против H1. 2) Приведите (с доказательством) основные свойства
    критерия. 3) Приведите (с выводом) выражение для P-значения критерия

    pvoin_mu_izv_var_b()
    11. По выборке X1, X2, . . . , Xn объема n из нормального закона распределения N(µ; σ2), когда µ = E(X)
    – известно, проверяется на уровне значимости α основная гипотеза H0 : σ = σ0 против альтернативной гипотезы H1 : σ > σ0. 
    1) Приведите необходимую статистику критерия и критическое
    множество для проверки H0 против H1. 2) Приведите (с доказательством) основные свойства критерия. 
    3) Приведите (с выводом) выражение для P-значения критерия

    pvoin_mu_izv_var_m()
    12. По выборке X1, X2, . . . , Xn объема n из нормального закона распределения N(µ; σ2), когда µ = E(X)
    – известно, проверяется на уровне значимости α основная гипотеза H0 : σ = σ0 против альтернативной гипотезы H1 : σ < σ0. 
    1) Приведите необходимую статистику критерия и критическое
    множество для проверки H0 против H1. 2) Приведите (с доказательством) основные свойства критерия. 
    3) Приведите (с выводом) выражение для P-значения критерия

    pvoin_mu_izv_var_n()
    13. По выборке X1, X2, . . . , Xn объема n из нормального закона распределения N(µ; σ2), когда µ = E(X)
    – известно, проверяется на уровне значимости α основная гипотеза H0 : σ = σ0 против альтернативной гипотезы H1 : σ =/= σ0. 
    1) Приведите необходимую статистику критерия и критическое
    множество для проверки H0 против H1. 2) Приведите (с доказательством) основные свойства критерия. 
    3) Приведите (с выводом) выражение для P-значения критерия

    pvoin_mu_neizv_var_b()
    14. По выборке X1, X2, . . . , Xn объема n из нормального закона распределения N(µ; σ2), когда µ = E(X)
    – неизвестно, проверяется на уровне значимости α основная гипотеза H0 : σ = σ0 против альтернативной гипотезы H1 : σ > σ0. 
    1) Приведите необходимую статистику критерия и критическое
    множество для проверки H0 против H1. 2) Приведите (с доказательством) основные свойства критерия. 
    3) Приведите (с выводом) выражение для P-значения критерия.

    pvoin_mu_neizv_var_m()
    15. По выборке X1, X2, . . . , Xn объема n из нормального закона распределения N(µ; σ2), когда µ = E(X)
    – неизвестно, проверяется на уровне значимости α основная гипотеза H0 : σ = σ0 против альтернативной гипотезы H1 : σ < σ0. 
    1) Приведите необходимую статистику критерия и критическое
    множество для проверки H0 против H1. 2) Приведите (с доказательством) основные свойства критерия. 
    3) Приведите (с выводом) выражение для P-значения критерия.

    pvoin_mu_neizv_var_n()
    16. По выборке X1, X2, . . . , Xn объема n из нормального закона распределения N(µ; σ2), когда µ = E(X)
    – неизвестно, проверяется на уровне значимости α основная гипотеза H0 : σ = σ0 против альтернативной гипотезы H1 : σ =/= σ0. 
    1) Приведите необходимую статистику критерия и критическое
    множество для проверки H0 против H1. 2) Приведите (с доказательством) основные свойства критерия. 
    3) Приведите (с выводом) выражение для P-значения критерия.

    pdnvo_var_izv_mu_b()
    17. По двум независимым выборкам X1, X2, . . . , Xn объема n из N(µX; X) и Y1, Y2, . . . , Ym объема m из N(µY ; σ2Y), 
    когда σ2X = Var(X) и σ2Y = Var(Y ) – известны, проверяется на уровне значимости α
    основная гипотеза H0 : µX = µY против альтернативной гипотезы H1 : µX > µY . 1) Приведите
    необходимую статистику критерия и критическое множество для проверки H0 против H1. 
    2) Приведите (с доказательством) основные свойства критерия. 3) Приведите (с выводом) выражение для P-значения критерия.

    pdnvo_var_izv_mu_n()
    18. По двум независимым выборкам X1, X2, . . . , Xn объема n из N(µX; σ2X) и Y1, Y2, . . . , Ym объема m из N(µY ; σ2Y), 
    когда σ2X = Var(X) и σ2Y = Var(Y ) – известны, проверяется на уровне значимости α
    основная гипотеза H0 : µX = µY против альтернативной гипотезы H1 : µX =/= µY . 1) Приведите
    необходимую статистику критерия и критическое множество для проверки H0 против H1. 
    2) Приведите (с доказательством) основные свойства критерия. 3) Приведите (с выводом) выражение для P-значения критерия.

    pdnvo_var_neizv_ravn_mu_b()
    19. По двум независимым выборкам X1, X2, . . . , Xn объема n из N(µX; σ2X) и Y1, Y2, . . . , Ym объема m из N(µY ; σ2Y) 
    c неизвестными, но равными дисперсиями σ2X = σ2Y = σ2, проверяется на уровне значимости α основная гипотеза H0 : µX = µY против 
    альтернативной гипотезы H1 : µX > µY . 1) Приведите необходимую статистику критерия и критическое множество для 
    проверки H0 против H1. 2) Приведите (с доказательством) основные свойства критерия. 
    3) Приведите (с выводом) выражение для P-значения критерия.

    pdnvo_var_neizv_ravn_mu_n()
    20. По двум независимым выборкам X1, X2, . . . , Xn объема n из N(µX; σ2X) и Y1, Y2, . . . , Ym объема m из N(µY ; σ2Y) 
    c неизвестными, но равными дисперсиями σ2X = σ2Y = σ2, проверяется на уровне значимости α основная гипотеза H0 : µX = µY против 
    альтернативной гипотезы H1 : µX =/= µY . 1) Приведите необходимую статистику критерия и критическое множество для проверки 
    H0 против H1. 2) Приведите (с доказательством) основные свойства критерия. 
    3) Приведите (с выводом) выражение для P-значения критерия.

    pdnvo_var_neizv_neravn_mu_n()
    21. По двум независимым выборкам X1, X2, . . . , Xn объема n из N(µX; σ2X) и Y1, Y2, . . . , Ym объема m из N(µY ; σ2Y) 
    c неизвестными и не равными дисперсиями, проверяется на уровне значимости α основная гипотеза H0 : µX = µY против 
    альтернативной гипотезы H1 : µX =/= µY (проблема БеренсаФишера). 1) Приведите статистику критерия Уэлча и критическое 
    множество для проверки H0против H1. 
    2) Приведите основное свойство статистики критерия. 3) Приведите (с выводом) выражение для P-значения критерия.

    pdnvo_var_b()
    22. По двум независимым выборкам X1, X2, . . . , Xn объема n из N(µX; σ2X) и Y1, Y2, . . . , Ym объема m из N(µY ; σ2Y) 
    проверяется на уровне значимости α основная гипотеза H0 : σ2X = σ2Y против альтернативной гипотезы H1 : σ2X > σ2Y. 
    1) Приведите необходимую статистику критерия и критическое множество для проверки H0 против H1. 
    2) Приведите (с доказательством) основные свойства критерия. 3) Приведите (с выводом) выражение для P-значения критерия.

    pdnvo_var_n()
    23. По двум независимым выборкам X1, X2, . . . , Xn объема n из N(µX; σ2X) и Y1, Y2, . . . , Ym объема m из N(µY ; σ2Y) 
    проверяется на уровне значимости α основная гипотеза H0 : σ2X = σ2Y против альтернативной гипотезы H1 : σ2X =/= σ2Y. 
    1) Приведите необходимую статистику критерия и критическое множество для проверки H0 против H1. 
    2) Приведите (с доказательством) основные свойства критерия. 3) Приведите (с выводом) выражение для P-значения критерия.

    pdnvo_var_neizv_ravn_mu_n_F()
    24. По двум независимым выборкам X1, X2, . . . , Xn объема n из N(µX; σ2X) и Y1, Y2, . . . , Ym объема m
    из N(µY ; σ2Y) c неизвестными, но равными дисперсиями σ2X = σ2Y = σ2, проверяется на уровне значимости α основная гипотеза 
    H0 : µX = µY против альтернативной гипотезы H1 : µX =/= µY. 1) Приведите необходимую статистику F – критерия 
    однофакторного дисперсионного анализа и критическое множество для проверки H0 против H1. 
    2) Приведите (с выводом и необходимыми пояснениями в обозначениях) обоснование 
    равенства процентных точек fα(1; n + m − 2) распределения Фишера и 
    t2α2(n + m − 2) распределения Стьюдента с (n + m − 2) свободы
    ''')
    
def help_q3():
    print('''
    Q3
    pvirrno()
    1) Пусть X1, X2, . . . , X6 – выборка из равномерного распределения на отрезке 
    [5;8], Fb(x) – соответствующая выборочная функция распределения. 
    Найдите: а) вероятность PFb(6) = Fb(8); б) вероятность PFˆ(7) =1/2
    
    ivoig()
    2) Имеется выборка X1,X2,...,Xn объема n из генеральной совокупности с функцией распределения F (x). 
    Найдите функции распределения экстремальных статистик X(1) и X(n)
    
    pidnn()
    3)Пусть X и Y – две независимые несмещенные оценки параметра θ с дисперсиями σ2 и 4σ2 соответственно. 
    a) Является ли X2 несмещенной оценкой параметра θ2? 
    б) Является ли Z = X · Y несмещенной оценкой параметра θ2?
    
    popas()
    4) Пусть θ = T(X1,...,Xn) оценка параметра θ, а b = (E[θ] − θ) – смещение. 
    Доказать формулу ∆ = Var(θ) + b^2, где ∆ = E[(θ − θ)^2 ] – среднеквадратичная ошибка оценки
    
    pvoinrsg()
    5) Пусть X1 , X2 – выборка объема 2 из некоторого распределения с генеральным средним θ = E(X ) и дисперсией σ2 = Var(X). 
    В качестве оценки параметра θ используется оценка вида θb = aX1 +2aX2.
    Известно отношение σ2/θ2 =3/5.Найдите оценку с наименьшей среднеквадратической ошибкой.
    Является ли эта оценка несмещенной?
    
    pvoirsm()
    6) Пусть X1, X2, . . . , Xn – выборка объема n из распределения с моментами ν1 = ν1(X) = E(X),
    μ2 = μ2(X) = σ2 = Var(X), μk = μk(X) = E[(X − E(X))^k], k = 3, 4. Покажите, что 
    a) μ3(X) = μ3(X)/n;
    b) μ4(X) = μ4(X)/n^3 + 3(n − 1)μ2^2(X)/n^3.
    
    pvigrsmo()
    7) Пусть X1, X2, X3 – выборка из генерального распределения с математическим ожиданием μ и дисперсией θ = σ2.
    Рассмотрим две оценки параметра θ:
    a)θ1 = c1(X1 −X2)^2;
    б)θ2 = c2[(X1 −X2)^2 + (X1 −X3)^2+(X2 −X3)^2].
    Найдите значения c1 и c2 такие,что оценки θb иθb являются несмещенными оценками параметра дисперсии σ2.
    
    pvird()
    8) Пусть X1, X2, X3, X4 – выборка из N(θ; σ 2 ). 
    Рассмотрим две оценки параметра θ: θb1 = (X1+2X2+3X3+4X4)/10 , θb2 = (X1+4X2+4X3+X4)/10 . 
    a) Покажите, что обе оценки являются несмещенными для параметра θ; 
    б) Какая из этих оценок является оптимальной?
    
    pvigri()
    9)  Пусть X1, X2, . . . , Xn – выборка из генерального распределения и пусть θ = E(X), σ2 = Var(X) – математическое ожидание
    и дисперсия. Рассмотрим следующие оценки параметра θ: θ1 = (X1 +X2)/2, θ2 = (X1 +Xn)/4+ (X2 +...+Xn−1)/2(n-2), θ3 = X . 
    а) Будут ли эти оценки несмещенными для параметра θ? 
    б) Какая из них является состоятельной для параметра θ?
    
    pvirr_drob()
    10) Пусть X1, X2, . . . , Xn – выборка из равномерного распределения U([0; θ]) 
    c неизвестным параметром θ > 0. 
    Требуется оценить параметр θ. 
    В качестве оценка параметра θ рассматриваются: θ1 =2X, θ2 = (n+1)/nX(n). 
    а)Будут ли оценки несмещенными? ;
    б)состоятельными? 
    в)найдитесреди них оптимальную. 
    
    pvirr_umnozh()
    11) Пусть X1, X2, . . . , Xn – выборка из равномерного распределения U([0; θ]) c неизвестным параметром θ > 0.
    Требуется оценить параметр θ. В качестве оценка параметра θ рассматриваются: 
    θ1 = 2X, θ2 =(n+1)X(1). 
    а)Будут ли оценки несмещенными?; б)Состоятельными? в)Найтисреди них оптимальную
    
    psvki()
    12) Пусть X – случайная величина, которая имеет равномерное распределение на отрезке [0, θ]. 
    Рассмотрим выборку объема 3 и класс оценок вида θb = c · X неизвестного параметра θ. 
    Найдите такое c, чтобы: 
    a) оценка θb – несмещенная; б) оценка θb – эффективная в рассматриваемом классе.
    
    pvoirz()
    13) Пусть X1, X2, . . . , Xn – выборка объема n из равномерного закона распределения на отрезке [−θ; θ], 
    где θ > 0 – неизвестный параметр. В качестве оценки параметра θ2 рассмотрим статистику 
    θb = 3/n (X12 + X22 + . . . + Xn2). Является ли статистика θbнесмещенной оценкой параметра θ2? 
    Является статистика θˆ несмещенной оценкой параметра √θ2 = θ? Ответ обосновать.
    
    pgnka_bez_skob()
    14) Пусть Yk = βxk + εk, k = 1, . . . n, где xk – некоторые константы, 
    а εk – независимые одинаково распределенные случайные величины, εk ∼ N (0; σ2 ). 
    Является ли оценка β = EYk/Exi несмещенной оценкой параметра β? Ответ обосновать.
    
    pgnka_so_skob()
    15) Пусть Yk = βxk + εk, k = 1, . . . n, где xk – некоторые константы, 
    а εk – независимые одинаково распределенные случайные величины, εk ∼ N (0; σ2 ). 
    Является ли оценка β = E(Yk/xi) несмещенной оценкой параметра β? Ответ обосновать.
    
    vtpdp()
    16)  В таблице представлены данные по числу сделок на фондовой бирже за квартал для 400 инвесторов:
    xi 0 1 2 3 4 5 6 7 8 9 10 ni 14697733423106333 2
    В предположении, что случайное число сделок описывается распределением Пуассона, 
    оцените параметр λ методом моментов. 
    Определите вероятность того, что число сделок за квартал будет не менее трех, применяя: 
    а) метод моментов; б) непосредственно по таблице.
    
    psvrrno04()
    17) Пусть случайная величина X равномерно распределена на отрезке [0; 4θ]. 
    Найдите методом мо- ментов оценку для параметра θ. Является ли оценка 
    а) несмещенной; б) состоятельной? Ответ обосновать.
    
    psvrrnoab()
    18) Пусть случайная величина X равномерно распределена на отрезке [a;b].
    Найти методом моментов оценки для параметров a и b.
    
    svssi()
    19.Случайная величина X (срок службы изделия) имеет распределение, плотность которого задается формулой f(x) = ...
    
    ichdvp()
    20.Известно, что доля возвратов по кредитам в банке имеет распределение F(x) = ... Наблюдения показали, что в среднем она составляет 78%. Методом моментов оцените параметр β и вероятность того, что она опуститься ниже 67%.
    
    pvoirp()
    21.Пусть X1, X2, . . . , Xn – выборка объема n из распределения Пуассона с параметром λ: P(X = k) =λ^k*e^−λ/k!, k = 0, 1, 2, . . . Найдите методом максимального правдоподобия по выборке x1, x2, . . . , xn точечную оценку неизвестного параметра λ распределения Пуассона.
    
    nmmpp()
    22.Найдите методом максимального правдоподобия по выборке x1, x2, . . . , xn точечную оценку λb неизвестного параметра λ показательного закона распределения, плотность которого f(x) = λe^−λx, x >0.
    
    nopip()
    23.Найдите оценки параметров a и b по методу максимального правдоподобия для равномерного распределения U([a, b]).
    
    pvidr()
    24.Пусть X1, X2, . . . , Xn – выборка из дискретного распределения P(X = −1) = θ, P(X = 1) = 4θ, P(X =2) = 2θ, P(X = 0) = 1 − 7θ, θ ∈ (0; 17). Найдите оценку параметра θ по методу максимального правдоподобия. Является ли полученная оценка: а) несмещенной; б) состоятельной. Ответ обосновать.
    
    pochss()
    25.Пусть ˆf – оценка числа степеней свободы f вида ˆf = ... Покажите, что min(n − 1; m − 1) 6 ˆf 6 n + m − 2.
    
    pvptr()
    26.Пусть fα(1; m) – (верхняя) процентная точка распределения Фишера с 1 и m степенями свободы, (m) – (верхняя) процентная точка распределения Стьюдента с m степенями свободы. Покажите,что
    
    inzkk()
    27.Инвестор наблюдает за колебаниями котировок акций компаний A и B в течение 100 торговых дней (по закрытию торгов). В результате наблюдений получена следующая статистика: количество дней, когда обе котировки падали – 26;обе котировки росли – 25; котировки падали, а котировки при этом росли – 29; наоборот, котировки росли, а котировки падали – 20. При 1% -муровне значимости проверьте гипотезу о равновероятности указанных четырех комбинаций падения и роста.
    
    vdzchs()
    28.В десятичной записи числа π среди 10 002 первых десятичных знаков после запятой цифры 0; 1; . . . ; 9 встречаются соответственно 968; 1026; 1021; 974; 1012; 1047; 1022; 970; 948; 1014 раз. На 5%-ом уровне значимости проверить гипотезу о равновероятности «случайных» чисел 0; 1; . . . ; 9, т.е. согласуются ли данные с гипотезой H0 : p0 = p1 = . . . p9 = 1/10 ? Найдите P-значение критерия.
    
    sschchn()
    29.Среди 10 000 «случайных чисел» 0, 1, . . . , 9, числа, не превосходящие 4, встретились k = 5089 раз. Проверить на уровне значимости α = 0, 1, согласуются ли эти данные с гипотезой H0 о равновероятности чисел. При каком уровне значимости эта гипотеза отвергается.
    
    pnisi()
    30.При 8002 независимых испытаний события A, B и C, составляющие полную группу, осуществились 2014, 5008 и 980 раз соответственно. Верна ли на уровне значимости 0, 05 гипотеза p(A) = 0, 5 − 2θ; p(B) = 0, 5 + θ; p(C) = θ (0 < θ < 0, 25)?
    
    ptsdp()
    31.Пусть таблица сопряженности двух признаков имеет вид
    Y = y1 Y = y2
    X = x1 a b
    X = x2 c d
    Показать, что статистика критерия χ2 Пирсона для проверки гипотезы независимости X и Y можно найти по формуле
    
    chdzpzchi2()
    32.Число π до 30 знака после запятой имеет вид: 3, 141592653589793238462643383279. Число e до 30 знака после запятой имеет вид: 2, 718281828459045235360287471352. Используя критерий однородности χ2, проверьте на уровне значимости α = 0, 05 гипотезу H0 о том, что последовательности цифр после запятой для обоих чисел принадлежат одной генеральной совокупности.
    
    itschv()
    33.Из таблицы случайных чисел выбрано n = 150 двузначных чисел. Частоты ni чисел, попавших в интервал [10i; 10i + 9],(i = 0, 1, . . . , 9) равны: (16; 15; 19; 13; 14; 19; 14; 11; 13; 16). Проверить, используя критерий Колмогорова, гипотезу H0 о согласии выборки с законом равномерного распределения. Уровень значимости α принять равным 0, 01.
    
    chdzpzks()
    34.Число π до 30 знака после запятой имеет вид:3, 141592653589793238462643383279. Число e до 30 знака после запятой имеет вид:2, 718281828459045235360287471352. Используя критерий однородности Колмогорова–Смиронова, проверьте на уровне значимости α = 0, 05 гипотезу H0 о том, что последовательности цифр после запятой для обоих чисел принадлежат одной генеральной совокупности.
    
    svichb()
    35. Случайная выборка из 395 человек была разделена по возрастному признаку, а также по тому, переключают ли люди телевизионные каналы во время просмотра передачи. Данные исследования представлены в следующей таблице:
    Переключение \ Возраст 18–24 25–34 35–49 50–64
    Да 60 54 46 41
    Нет 40 44 53 57
    Используя приведенные данные, проверьте гипотезу о том, что переключение каналов и возраст являются независмимыми признаками в случае, когда a) α = 5%; б) α = 2, 5%. Найдите P-значениекритерия.
    ''')
    
def help_q4_q5_q6():
    print('''
    Q4
    1) Условные характеристики относительно дискретной СВ
    vpbun_modumo() 
    1. В первом броске участвуют 160 несимметричных монет. Во втором броске участвуют только те монеты, на которых в первом броске выпал "орел". Известно, что вероятность выпадения "орла" для данных несимметричных монет равна 0,55. Найдите: 1) математическое ожидание числа "орлов", выпавших во втором броске; 2) дисперсию условного математического ожидания числа "орлов", выпавших во втором броске, относительно числа "орлов", выпавших в первом броске
    
    vpbun_momoud()
    2. В первом броске участвуют 79 несимметричных монет. Во втором броске участвуют только те монеты, на которых в первом броске выпал "орел". Известно, что вероятность выпадения "орла" для данных несимметричных монет равна 0,6. Найдите: 1) математическое ожидание числа "орлов", выпавших во втором броске; 2) математическое ожидание условной дисперсии числа "орлов", выпавших во втором броске, относительно числа "орлов", выпавших в первом броске.
    
    vpbun_mouddumo()
    3. В первом броске участвуют 88 несимметричных монет. Во втором броске участвуют только те монеты, на которых в первом броске выпал "орел". Известно, что вероятность выпадения "орла" для данных несимметричных монет равна 0,7. Найдите: 1) математическое ожидание условной дисперсии числа "орлов", выпавших во втором броске, относительно числа "орлов", выпавших в первом броске; 2) дисперсию условного математического ожидания числа "орлов", выпавших во втором броске, относительно числа "орлов", выпавших в первом броске.
    
    suoop()
    4. Средний ущерб от одного пожара составляет 4,4 млн. руб. Предполагается, что ущерб распределен по показательному закону, а число пожаров за год - по закону Пуассона. Также известно, что за 5 лет в среднем происходит 14 пожаров. Найдите: 1) математическое ожидание суммарного ущерба от всех пожаров за один год; 2) стандартное отклонение суммарного ущерба от пожаров за год.
    
    muoss()
    5. Максимальный ущерб от страхового случая составляет 3,3 млн. руб. Предполагается, что фактический ущерб распределен равномерно от 0 до максимального ущерба, а число страховых случаев за год - по закону Пуассона. Также известно, что за 10 лет в среднем происходит 12 страховых случаев. Найдите: 1) математическое ожидание суммарного ущерба от всех страховых случаев за один год; 2) стандартное отклонение суммарного ущерба от страховых случаев за год.
    
    dstsiv()
    6. Для случайной цены Y известны вероятности: P(Y=2)=0,6 и P(Y=15)=0,4. При условии, что Y=y, распределение выручки X является равномерным на отрезке [0,7y]. Найдите: 1) математическое ожидание E(XY); 2) ковариацию Cov(X,Y).
    
    ikimp()
    7. Игральная кость и 29 монет подбрасываются до тех пор, пока в очередном броске не выпадет ровно 8 "орлов". Пусть S – суммарное число очков, выпавших на игральной кости при всех бросках. Найдите: 1) математическое ожидание E(S); 2) стандартное отклонение σS.
    
    2) Эмпирические характеристики
    vgusi()
    1. В группе учится 29 студентов. Ими были получены следующие 100-балльные оценки: 90, 79, 53, 62, 66, 68, 75, 0, 82, 29, 0, 29, 68, 90, 0, 60, 44, 44, 70, 68, 70, 89, 0, 68, 0, 66, 0, 59, 70. Найдите: 1) A – среднюю положительную оценку в группе; 2) M – медиану положительных оценок в группе; 3) H – среднее гармоническое и G – среднее геометрическое оценок, которые не менее M; 4) Q – медианную оценку в той части группы, в которой студенты набрали не менее M баллов; 5) N – количество студентов, оценки которых оказались между H и Q (включая границы).
    
    scheun()
    2. Следующие 28 чисел – это умноженные на 10000 и округленные до ближайшего целого дневные логарифмические доходности акции компании АВС: -9, 9, -138, -145, 186, 78, 34, -37, -19, -68, -82, 158, 96, -189, 24, 84, -99, 125, -39, 26, 62, -91, 239, -211, 2, 129, 2, -16. Будем называть их преобразованными доходностями (ПД). Финансовый аналитик Глеб предполагает, что преобразованные доходности (как и исходные) приближенно распределены по нормальному закону. Чтобы проверить свое предположение Глеб нашел нижнюю квартиль L и верхнюю квартиль H нормального распределения N(μ,σ2), для которого μ – это среднее арифметическое ПД, а σ – эмпирическое стандартное отклонение ПД. Затем Глеб подсчитал количество ПД, попавших в интервал от L до H (надеясь, что в этот интервал попадет половина ПД). Результат этого вычисления показался ему недостаточно убедительным. Чтобы окончательно развеять сомнения относительно нормальности ПД, Глеб построил на одном рисунке графики функций: F^(x) и F(x), где F^(x) – эмпирическая функция распределения ПД, а F(x) – функция распределения N(μ,σ2). В качестве меры совпадения двух графиков Глеб решил использовать расстояние d между функциями F^(x) и F(x) , которое он вычислил, исходя из определения: d=sup|F^(x)−F(x)|. В ответе укажите результаты вычислений Глеба: 1) среднее арифметическое ПД; 2) эмпирическое стандартное отклонение ПД; 3) квартили L и H; 4) количество ПД, попавших в интервал от L до H; 5) расстояние между функциями F^(x) и F(x).
    
    vgusp_kkk()
    3. В группе Ω учатся студенты: ω1,...,ω30 . Пусть X и Y – 100-балльные экзаменационные оценки по математическому анализу и теории вероятностей. Оценки студента ωi обозначаются: xi=X(ωi) и yi=Y(ωi) , i=1,...,30 . Все оценки известны: x1=71,y1=71 , x2=52,y2=58 , x3=72,y3=81 , x4=87,y4=92 , x5=81,y5=81 , x6=100,y6=94 , x7=90,y7=96 , x8=54,y8=46 , x9=54,y9=60 , x10=58,y10=62 , x11=56,y11=49 , x12=70,y12=60 , x13=93,y13=86 , x14=46,y14=48 , x15=56,y15=61 , x16=59,y16=52 , x17=42,y17=40 , x18=60,y18=60 , x19=33,y19=37 , x20=83,y20=92 , x21=50,y21=57 , x22=93,y22=93 , x23=41,y23=42 , x24=55,y24=64 , x25=60,y25=59 , x26=37,y26=30 , x27=71,y27=71 , x28=42,y28=44 , x29=85,y29=82 , x30=39,y30=39 . Требуется найти следующие условные эмпирические характеристики: 1) ковариацию X и Y при условии, что одновременно X⩾50 и Y⩾50 ; 2) коэффициент корреляции X и Y при том же условии.
    
    psign()
    4. Поток Ω состоит из k групп: Ω1,...,Ωk , k=3 . На потоке учатся n=n1+...+nk студентов, где ni – число студентов в группе Ωi , i=1,...,k . Пусть X(ω) – 100-балльная оценка студента ω∈Ω . Далее используются следующие обозначения: x¯¯¯i – среднее значение, σi – (эмпирическое) стандартное отклонение признака X на группе Ωi . Дано: n1=24 , n2=26 , n3=30 , x¯¯¯1=70 , x¯¯¯2=76 , x¯¯¯3=77 , σ1=4 , σ2=6 , σ3=8 . Требуется найти: 1) среднее значение X на потоке Ω ; 2) (эмпирическое) стандартное отклонение X на потоке Ω .
    
    3) Выборки из конечной совокупности
    vgusp_dtsm()
    1. В группе Ω учатся 27 студентов, Ω={1,2,...,27} . Пусть X(i) – 100-балльная оценка студента i∈Ω . Из группы Ω случайным образом 7 раз выбирается студент ω∈Ω . Повторный выбор допускается. Пусть ωj – студент, полученный после выбора j=1,...,7 , X(ωj) – его оценка. Среднюю оценку на случайной выборке обозначим X¯¯¯¯=17∑X(ωj) . Оценки в группе даны: 100, 86, 51, 100, 95, 100, 12, 61, 0, 0, 12, 86, 0, 52, 62, 76, 91, 91, 62, 91, 65, 91, 9, 83, 67, 58, 56. Требуется найти: 1) дисперсию Var(X¯¯¯¯) ; 2) центральный момент μ3(X¯¯¯¯).
    
    vgusp_mod()
    2. В группе Ω учатся 27 студентов, Ω={1,2,...,27} . Пусть X(i) – 100-балльная оценка студента i∈Ω . Из группы Ω случайным образом 6 раз выбирается студент ω∈Ω . Повторный выбор не допускается. Пусть ωj – студент, полученный после выбора j=1,...,6 , X(ωj) – его оценка. Среднюю оценку на случайной выборке обозначим X¯¯¯¯=16∑X(ωj) . Оценки в группе даны: 100, 78, 77, 51, 82, 100, 73, 53, 78, 55, 7, 0, 81, 15, 96, 12, 71, 70, 53, 0, 73, 100, 55, 100, 59, 89, 81. Требуется найти: 1) математическое ожидание E(X¯¯¯¯) ; 2) дисперсию Var(X¯¯¯¯) .
    
    rbned()
    3. Распределение баллов на экзамене до перепроверки задано таблицей Оценка работы: 2,3,4,5 Число работ: 7, 48, 8, 105 Работы будут перепроверять 6 преподавателей, которые разделили все работы между собой поровну случайным образом. Пусть X¯¯¯¯ – средний балл (до перепроверки) работ, попавших к одному из преподавателей. Требуется найти: 1) математическое ожидание E(X¯¯¯¯) ; 2) стандартное отклонение σ(X¯¯¯¯) .
    
    dikki()
    4. Две игральные кости, красная и синяя, подбрасываются до тех пор, пока не выпадет 19 различных (с учетом цвета) комбинаций очков. Пусть Ri – число очков на красной кости, а Bi – число очков на синей кости в комбинации с номером i . Случайные величины Xi задаются соотношениями: Xi=11Ri−9Bi,i=1,...,19 . Среднее арифметическое этих величин обозначим X¯¯¯¯=1/19 ∑Xi . Требуется найти: 1) математическое ожидание E(X¯¯¯¯) ; 2) стандартное отклонение σ(X¯¯¯¯) .
    
    ipmmp()
    5. Имеется 11 пронумерованных монет. Монеты подбрасываются до тех пор, пока не выпадет 257 различных (с учетом номера монеты) комбинаций орел-решка. Пусть Xi – число орлов в комбинации с номером i ; а X¯¯¯¯=1257∑Xi – среднее число орлов в полученных таким образом комбинациях. Требуется найти: 1) математическое ожидание E(X¯¯¯¯) ; 2) дисперсию Var(X¯¯¯¯) .
    
    erpin_modkk()
    6. Эмпирическое распределение признаков  𝑋 и  𝑌 на генеральной совокупности  Ω={1,2,...,100} задано таблицей частот 𝑋=100𝑋=400𝑌=11124𝑌=23211𝑌=31111.  Из  Ω случайным образом без возвращения извлекаются 7 элементов. Пусть  𝑋⎯⎯⎯⎯⎯ и  𝑌⎯⎯⎯⎯ – средние значения признаков на выбранных элементах. Требуется найти: 1) математическое ожидание  E(𝑌⎯⎯⎯⎯); 2) дисперсию Var(Y¯¯¯¯); 3) коэффициент корреляции ρ(X¯¯¯¯,Y¯¯¯¯).
    
    erpin_mosok()
    7. Эмпирическое распределение признаков  𝑋 и  𝑌 на генеральной совокупности  Ω={1,2,...,100} задано таблицей частот 𝑋=100𝑋=300𝑌=12110𝑌=21727𝑌=41213. Из  Ω случайным образом без возвращения извлекаются 6 элементов. Пусть  𝑋⎯⎯⎯⎯⎯ и  𝑌⎯⎯⎯⎯ – средние значения признаков на выбранных элементах. Требуется найти: 1) математическое ожидание  E(𝑌⎯⎯⎯⎯); 2) стандартное отклонение  𝜎(𝑋⎯⎯⎯⎯⎯); 3) ковариацию  Cov(𝑋⎯⎯⎯⎯⎯,𝑌⎯⎯⎯⎯)
    
    4) Метод максимального правдоподобия
    iielp()
    1. Глеб и Анна исследуют эффективность лекарственного препарата АВС. Глеб, используя модель Анны, создал компьютерную программу, вычисляющую по заданным генетическим факторам вероятность (в процентах) успешного применения АВС. Программа Глеба накапливает полученные вероятности и в итоге выдает набор частот: n0,n1,...,n100 . Например, n75 – это число случаев, в которых программа Глеба получила вероятность 75%. Обработав 1000 образцов генетического материала, Анна нашла значения факторов и ввела их в программу. В результате был получен следующий набор частот: 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 1, 1, 3, 4, 4, 5, 4, 6, 6, 11, 9, 19, 23, 25, 33, 36, 36, 46, 46, 49, 58, 90, 76, 66, 69, 75, 68, 44, 39, 21, 16, 5, 2, 1, 0, 0, 0. Для завершения этапа исследования необходимо было подобрать распределение, соответствующее полученным частотам. Анна решила использовать распределение на отрезке [0,1] с плотностью f(x)=f(x;a,b)=abxa−1(1−xa)b−1 и целочисленными параметрами a,b в диапазоне от 1 до 20. В результате максимизации функции правдоподобия (при указанных ограничениях) Глебом были получены значения параметров: a^=A и b^=B . Задача: пусть X – случайная величина, распределения на отрезке [0,1] с плотностью f(x)=f(x;a^,b^) , F(x) – ее функция распределения. Требуется найти математическое ожидание E(X) и X0, 2=F−1(0,2) – квантиль уровня 0,2. Какой смысл для всей популяции имеют E(X) и X0, 2 ? В ответе укажите: 1) значение A ; 2) значение B ; 3) математическое ожидание E(X) ; 4) квантиль X0, 2 .
    
    5) Доверительный интервал для коэффицента корреляции
    prsvid()
    1. Пусть (x1,y1);...;(x31,y31) – реализация случайной выборки (X1,Y1);...;(X31,Y31) из двумерного нормального распределения N(μx;μy;σ2x;σ2y;ρ) . Используя векторы x⃗ =(x1;...;x31) и y⃗ =(y1;...;y31) , постройте асимптотический 0,93- доверительный интервал (θˆ1;θˆ2) для коэффициента корреляции ρ . В ответе укажите: 1) выборочный коэффициент корреляции ρˆ; 2) верхнюю границу θˆ2 построенного доверительного интервала для ρ . Исходные данные: x⃗ = (-0,616; -0,238; 0,173; -0,255; 0,531; 0,718; -0,161; 0,371; -1,014; -0,413; -1,571; 0,485; 0,486; 0,688; -0,944; 0,155; 0,003; 0,111; 0,752; 0,783; -0,102; -0,74; -2,097; 1,349; -0,044; -0,617; -0,782; -0,873; -0,995; -1,256; -0,596), y⃗ = (-1,34; -0,25; 0,101; -0,626; -0,088; 0,539; -0,451; 0,233; -1,186; -0,423; -1,329; 0,231; 0,209; 0,638; -0,274; -0,491; -0,319; 0,294; 0,895; 1,164; -0,57; -1,078; -1,526; 1,491; 0,182; -0,31; -1,001; -0,969; -0,918; -0,904; -0,595).
    
    6) Проверка гипотез о значении среднего
    prsvin_z()
    1. Пусть x⃗ =(x1,…,x30) – реализация случайной выборки X⃗ =(X1,…,X30) из нормального распределения N(μ;3,42) . Проверяется на уровне значимости α=0,01 основная гипотеза H0:μ=1,29 против альтернативной гипотезы H1:μ≠1,29 с критическим множеством вида Kα=(−∞,−A)∪(A,+∞) . 1) Найдите значение статистики критерия Zнабл.=Z(x⃗ ) . 2) Найдите границу А критического множества. 3) Найдите P -значение критерия и сделайте выводы. 4) Найдите мощность W критерия для H1:μ=1,17 . Исходные данные: x⃗ = (1,416; 0,624; 6,471; 6,256; 1,787; 2,546; -1,758; -5,475; 0,077; 1,792; 5,443; 5,348; -0,057; 0,232; -2,305; -3,568; -4,541; 7,893; -0,473; -0,229; -3,0; 3,903; -4,227; 0,537; -1,785; 2,575; -0,477; -2,754; 1,164; 2,716).
    
    prsvin_t()
    2. Пусть x⃗ =(x1,…,x20) – реализация случайной выборки X⃗ =(X1,…,X20) из нормального распределения N(μ;σ2) . Проверяется на уровне значимости α=0,05 основная гипотеза H0:μ=1,10 против альтернативной гипотезы H1:μ≠1,10 с критическим множеством вида Kα=(−∞,−A)∪(A,+∞) . 1) Найдите значение статистики критерия t=Tнабл.=T(x⃗ ) . 2) Найдите границу А критического множества. 3) Найдите P-значение критерия и сделайте выводы. 4) Найдите мощность W критерия для H1:μ=0,91 . Исходные данные: x⃗ = (1,146; 2,958; -3,325; -0,534; 0,374; 5,293; 0,12; 1,185; 5,148; 5,351; 2,639; 1,47; -1,967; 4,96; 6,057; -0,542; 1,544; -0,243; -1,988; 2,844).

    7) Проверка гипотез о значении дисперсии
    prsvin_chi20()
    1. Пусть x⃗ =(x1,…,x30) – реализация случайной выборки X⃗ =(X1,…,X30) из нормального распределения N(1,18;σ2) . Проверяется на уровне значимости α=0,02 гипотеза H0:σ=1,14 против альтернативной гипотезы H1:σ≠1,14 с критическим множеством вида Kα=(0;A)∪(B;+∞) . 1) Найдите значение статистики критерия χ20 . 2) Найдите границы А и В критического множества и проверьте гипотезу H0 . 3) Найдите P-значение критерия. 4) Найдите вероятность ошибки второго рода β для σ1=1,24 . Исходные данные: x⃗ = (0,889; 1,514; 2,846; 2,811; 0,84; 0,945; 0,02; -0,441; -0,796; 3,739; 0,688; 0,777; -0,233; 2,284; -0,681; 1,056; 0,21; 1,8; 0,687; -0,144; 1,285; 1,851; 1,402; 1,695; 0,533; 0,87; 0,486; 0,874; 0,312; -0,821).
    
    prsvin_chi2()
    2. Пусть x⃗ =(x1,…,x30) – реализация случайной выборки X⃗ =(X1,…,X30) из нормального распределения N(μ;σ2) . Проверяется на уровне значимости α=0,02 гипотеза H0:σ=1,14 против альтернативной гипотезы H1:σ≠1,14 с критическим множеством вида Kα=(0;A)∪(B;+∞) . 1) Найдите значение статистики критерия χ2 . 2) Найдите границы А и В критического множества и проверьте гипотезу H0 . 3) Найдите P-значение критерия. 4) Найдите вероятность ошибки второго рода β для σ1=1,24 . Исходные данные: x⃗ = (0,889; 1,514; 2,846; 2,811; 0,84; 0,945; 0,02; -0,441; -0,796; 3,739; 0,688; 0,777; -0,233; 2,284; -0,681; 1,056; 0,21; 1,8; 0,687; -0,144; 1,285; 1,851; 1,402; 1,695; 0,533; 0,87; 0,486; 0,874; 0,312; -0,821).
    
    8) Проверка гипотез о равенстве двух средних
    prsvin_xy_z()
    1. Пусть x⃗ =(x1,…,x25) – реализация случайной выборки X⃗ =(X1,…,X25) из нормального распределения N(μx;0,72) , а y⃗ =(y1,…,y30) – реализация случайной выборки Y⃗ =(Y1,…,Y30) из нормального распределения N(μy;1,42) . Известно, что X⃗ и Y⃗ независимы. Проверяется гипотеза H0:μx=μy против альтернативной гипотезы H1:μx>μy . При уровне значимости α применяется критерий с критической областью {Z>A} , где статистика критерия Z=Z(X⃗ ,Y⃗ ) – это нормированная разность X¯−Y¯ , A=Aα – зависящее от α критическое значение. Соответствующее критическое множество имеет вид Kα=(Aα;∞) . 1) Найдите значение статистики критерия Zнабл.=Z(x⃗ ,y⃗ ) . 2) Найдите P -значение критерия. 3) Найдите критическое значение A , критическое множество Kα и проверьте гипотезу H0 при α=0,02 . 4) Найдите мощность критерия W в случае μx−μy=0,1 и α=0,02 . Исходные данные: x⃗ = (3,842; 3,374; 4,18; 4,5; 4,247; 4,412; 3,756; 3,946; 3,729; 3,948; 3,631; 2,992; 4,324; 3,919; 3,059; 4,524; 3,565; 4,236; 4,71; 4,29; 4,998; 3,336; 4,482; 3,721; 3,59); y⃗ = (3,19; 3,564; 4,079; 2,369; 5,261; 4,652; 1,849; 6,084; 6,654; 5,65; 3,748; 2,501; 5,476; 3,436; 5,711; 4,292; 5,367; 4,499; 4,989; 4,015; 6,5; 4,178; 4,563; 6,636; 2,113; 2,221; 5,357; 2,358; 6,721; 3,421).
    
    9) Проверка гипотез о равенстве трех средних
    dtgfp()
    1. Для трех групп финансовых показателей A: (X1;...;X27) , B: (Y1;...;Y33) , C: (Z1;...;Z39) , которые по предположению независимы и распределены, соответственно, по трем нормальным законам N(μx,σ2) , N(μy,σ2) , N(μz,σ2) (с одинаковой неизвестной дисперсией σ2 ) на уровне значимости α=0,01 с помощью F-критерия (Фишера) проверяется гипотеза H0:μx=μy=μz о совпадении ожидаемых значений показателей. Конкретные значения всех показателей указаны ниже. 1) По данным значениям показателей найдите межгрупповую дисперсию. 2) По этим же данным найдите среднюю групповую дисперсию. 3) Найдите значение статистики F-критерия, критическое множество Kα и проверьте гипотезу H0 . 4) Найдите P-значение критерия и сделайте выводы. Значения показателей группы A: (0,616; 1,046; 2,575; -0,344; 2,339; -0,68; 3,739; 2,251; -1,252; 3,536; -0,491; 5,556; 4,856; -1,68; 2,33; 1,345; 2,829; 2,539; 3,304; 3,497; 0,211; 3,563; 0,94; 3,642; 1,956; 3,919; 3,568). Значения показателей группы B: (2,834; 1,504; -0,678; 5,619; 0,97; 1,617; 3,768; -1,309; 3,343; -1,778; -0,854; 1,04; 2,83; -2,335; 4,853; 5,6; 4,341; 4,362; 3,52; 1,151; -0,621; -2,88; 1,697; 1,753; 0,211; 2,157; 1,989; 2,457; 1,399; 1,61; -0,558; 2,132; 2,293). Значения показателей группы C: (2,398; -2,77; 4,679; 1,924; 0,574; 5,329; 0,699; 4,457; -0,3; 1,682; -1,34; 0,046; -1,096; 1,935; 2,411; 4,134; 5,643; 3,071; 6,526; 4,941; 2,844; -0,43; -2,066; 0,22; 0,317; -1,923; 1,38; -2,485; 0,111; -0,542; 4,78; 1,93; 0,462; 5,487; -3,547; 2,933; -0,987; -0,21; 3,955).
    
    10) Из файла
    dtgfp_file()
    1. Для трех групп финансовых показателей A, B, C проверяется гипотеза о совпадении ожидаемых значений показателей. Предполагается, что все показатели Xij независимы и распределены по нормальному закону N(muj, sigma^2) с одинаковой неизвестной дисперсией Var(Xij)=sigma^2, причем для каждой группы E(Xij) = muj, j=1,2,3 . 1) По данным значениям (файл ds5.9.8.csv) найдите межгрупповую и среднюю групповую дисперсии. 2) Найдите 91% доверительные интервалы для ожидаемых значений показателей muj, j=1,2,3. 3) Найдите значение статистики критерия f0 = Fнабл, критическое множество Kalpha и на 3% уровне значимости проверьте гипотезу о совпадении ожидаемых значений показателей, mu1 = mu2 = mu3. 4) Найдите P-значение критерия и сделайте выводы.
    psvfr()
    2. По содержащейся в файле ds6.4.12.csv реализации случайной выборки из двумерного нормальногораспределения с неизвестными параметрами и : 1) запишите логарифм функции правдоподобия, ; 2) найдите оценки максимального правдободобия и .
    ''')
    
    
def tasks():
    im1 = Image.open(requests.get('https://sun9-47.userapi.com/impf/8qpySADYWFg7ZmRDfBlX_goezR7xS7Bf9ysloA/VNAI5FFEI38.jpg?size=535x604&quality=96&sign=dbebaed3445b5b917a5627271ee43a1d&type=album', stream=True).raw)
    im2 = Image.open(requests.get('https://sun9-25.userapi.com/impf/usp21U_ntFV4wOtRiaCGNTXDB2Yw69DUn_zbOg/YVs-HuQNTuA.jpg?size=548x651&quality=96&sign=818deed04a63ee1a6ac374a33ffb9eb7&type=album', stream=True).raw)
    im3 = Image.open(requests.get('https://sun9-42.userapi.com/impf/brYQzWvEIRe2m5-aH-mPRgh6-oX2Q6btL6P61A/Lhv-IrpYEfs.jpg?size=553x559&quality=96&sign=1a448c9a09593c9639a8057e7e3b8229&type=album', stream=True).raw)
    im4 = Image.open(requests.get('https://sun9-43.userapi.com/impf/kgz7EKcomW9gifgsRprRzBFgzEbkntNd31-u1w/-veWby6slbw.jpg?size=543x652&quality=96&sign=2b01d7459b52cb23c585865ffe7e2d52&type=album', stream=True).raw)
    im5 = Image.open(requests.get('https://sun9-5.userapi.com/impf/jrNA2gbjILui6NeNTyhu6OHhvihFi4Huw-vRDw/ZOdBn5YAeZ4.jpg?size=545x552&quality=96&sign=7838fe322c803e4202ca2a8ab20ec993&type=album', stream=True).raw)
    im6 = Image.open(requests.get('https://sun9-54.userapi.com/impf/ysc3CMWde8IClGiznpIvyoEckQW5LunsrcO02A/XEFXU41BXGI.jpg?size=550x594&quality=96&sign=033e539d3996317a1e217e7429c3d602&type=album', stream=True).raw)
    im7 = Image.open(requests.get('https://sun9-40.userapi.com/impf/XZsCiscgaQ7uTDYFcroBX1yx2s_iI8Bn36j5WA/bmSzaO4ENBI.jpg?size=547x639&quality=96&sign=2fa6e350da8808139ecd2bdbe0f1e45a&type=album', stream=True).raw)
    im8 = Image.open(requests.get('https://sun9-24.userapi.com/impf/ocx_hS_Cg_ZoP5kWnKrQgVGUdXcGH-R52_VQ3Q/aQBNpVfbQ5M.jpg?size=536x644&quality=96&sign=4ab20ebbaae6b412e952f3c548503195&type=album', stream=True).raw)
    im9 = Image.open(requests.get('https://sun9-72.userapi.com/impf/SW9nLnkG_wCo7v0VPRfTuYwLAi882AgBe4Hq3A/XjlmPePpQ9M.jpg?size=548x535&quality=96&sign=21f92389ec5e6432cb9b14372a1f94d2&type=album', stream=True).raw)
    im10 = Image.open(requests.get('https://sun9-45.userapi.com/impf/iYP7yjG1gXvMUANtvV9emZ6I3BCsiRna4Y_SgQ/LfdnbX896M0.jpg?size=553x650&quality=96&sign=68630ca277284d710114815a001e091b&type=album', stream=True).raw)
    im11 = Image.open(requests.get('https://sun9-10.userapi.com/impf/MdS4xrhxVvEScqWX0DaYFPbaR-BiQ6wAslfPPA/uuHSymnExW0.jpg?size=541x354&quality=96&sign=23567c39217e6914ef34197d01e7b4ef&type=album', stream=True).raw)
    return im1, im2, im3, im4, im5, im6, im7, im8, im9, im10, im11