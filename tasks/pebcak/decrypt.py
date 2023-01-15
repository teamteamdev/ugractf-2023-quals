encrypted_flag = "9N_GN_tN_wu_qY_xi_Md_08_zfN_ctN_HQE_O7w_vnf_xZb_1Gv_VB6_y6f_lNG_H5N_0Nr_xNo_dBG_09j_rZI_QwB_122_CHT_tE1_qDO_emd_0Za_xuV_I2Y_Bxd_WG6_Okb_sgS_7cb_GPO_cSx_y0L_OLb_4dN_fA1_s0i_DBk_8mT_xzq_z40_oXf_Jq6_ZZP"
code = "ANEcwu4fYegObF1i2VXyvJHxKd0qBkMl36ILRaUjPG8rToSZzpCDt7n9mWsh5Q"

def decode(s):
    n = 0
    for c in s[::-1]:
        n *= len(code)
        n += code.find(c)
    return n

numbers = [decode(s) for s in encrypted_flag.split("_")]

for i in range(len(numbers) - 1, 2, -1):
    numbers[i] = (numbers[i] - numbers[i-1] - numbers[i-2]) % 179179

print(bytes(numbers).decode())
