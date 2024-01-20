import numpy as np
def smooth(x,y, res = 44, ncf = 100):
  engy = x
  eps1 = y
  eps2 = y
  # Set parameters
  ki = 0
  kf = len(y-1)
  nc = ncf
  M = res
  THH = np.pi/2
  OFF = 2.0

  # Derived universal parameters
  NPTS = kf - ki 
  nmax = (NPTS - 1)//2
  nmax1 = nmax +1
  M1 = M +1
  j0 = (NPTS)//2
  THETC = 2*np.pi/NPTS
  FCON = 2/NPTS
  cosH = np.cos(THH)
  sinH = np.sin(THH)

  # Set up working vectors
  E = np.zeros(NPTS)
  eps = np.zeros(NPTS)
  eps20 = np.zeros(NPTS)
  for k in range(ki, kf):
      j = k - ki
      E[j] = engy[k]
      eps[j] = eps1[k]
      eps20[j] = eps2[k]

  # Set up line and parabola "spectra"
  LI = np.zeros(NPTS)
  PA = np.zeros(NPTS)
  THET = np.zeros(NPTS)
  for j in range(NPTS):
      TH = THETC*(j - j0)
      LI[j] = TH
      PA[j] = TH*TH
      THET[j] = TH

  # Layer 2: compute Fourier coefficients
  h = np.zeros(nmax1)
  AD = np.zeros(nmax1)
  BD = np.zeros(nmax1)
  lnCD = np.zeros(nmax1)
  phD = np.zeros(nmax1)
  B1 = np.zeros(nmax1)
  A2 = np.zeros(nmax1)
  for n1 in range(1, nmax1+1):
      n = n1 - 1
      h[n1 -1] = n
      S1 = 0
      S2 = 0
      S3 = 0
      S4 = 0
      for j in range(NPTS):
          TH = THETC*(j - j0)
          nTH = n*TH
          S1 += eps[j]*np.cos(nTH)
          S2 += eps[j]*np.sin(nTH)
          S3 += TH*np.sin(nTH)
          S4 += TH*TH*np.cos(nTH)
      AD[n1-1] = FCON*S1
      BD[n1-1] = FCON*S2
      lnCD[n1-1] = 0.5*np.log(AD[n1-1]**2 + BD[n1-1]**2)
      phD[n1-1] = np.arctan2(S2, S1)
      B1[n1-1] = FCON*S3
      A2[n1-1] = FCON*S4
  AD[0] /= 2
  A2[0] /= 2
  lnCD[0] = np.log(AD[0])

  # Check: do inverse transform
  epsR = np.zeros(NPTS)
  LIR = np.zeros(NPTS)
  PAR = np.zeros(NPTS)
  for j in range(NPTS):
      S1 = 0
      S3 = 0
      S4 = 0
      THj = THETC*(j - j0)
      for n1 in range(1, nmax1+1):
          n = n1 - 1
          S1 += AD[n1-1]*np.cos(n*THj) + BD[n1-1]*np.sin(n*THj)
          S3 += B1[n1-1]*np.sin(n*THj)
          S4 += A2[n1-1]*np.cos(n*THj)
      epsR[j] = S1
      LIR[j] = S3
      PAR[j] = S4

  # Layer 3: IRED
  S1 = 0
  S2 = 0
  S3 = 0
  S4 = 0
  nc1 = nc + 1
  for n1 in range(nc1, nmax1+1):
      S1 += AD[n1-1]*A2[n1-1]
      S2 += A2[n1-1]*A2[n1-1]
      S3 += BD[n1-1]*B1[n1-1]
      S4 += B1[n1-1]*B1[n1-1]
  if S4 == 0:
    c1 = 0
  else:
    c1 =S3/S4
  if S2 == 0:
    c2 = 0
  else:
    c2 =S1/S2


  ADI = np.zeros(nmax1)
  BDI = np.zeros(nmax1)
  lnCDI = np.zeros(nmax1)
  phDI = np.zeros(nmax1)
  for n1 in range(1, nmax1):
      ADI[n1-1] = AD[n1-1] - c2*A2[n1-1]
      BDI[n1-1] = BD[n1-1] - c1*B1[n1-1]
      lnCDI[n1-1] = 0.5*np.log(ADI[n1-1]**2 + BDI[n1-1]**2)
      phDI[n1-1] = np.arctan2(BDI[n1-1], ADI[n1-1])

  epsI = np.zeros(NPTS)
  for j in range(NPTS):
      epsI[j] = eps[j] - c1*LI[j] - c2*PA[j]

  # Layer 4, 5: Hilbert transform and Hilbert rotation
  ADH = np.zeros(nmax1)
  BDH = np.zeros(nmax1)
  RH = np.zeros(nmax1, dtype=complex)
  for n1 in range(1, nmax1 +1):
      ADH[n1-1] = ADI[n1-1]*cosH - BDI[n1-1]*sinH
      BDH[n1-1] = ADI[n1-1]*sinH + BDI[n1-1]*cosH
      RH[n1-1] = (ADH[n1-1] - 1j*BDH[n1-1])/2

  ADH[0] = ADI[0]
  BDH[0] = 0
  RH[0] = ADH[0] + OFF
  epsIH = np.zeros(NPTS)
  for j in range(NPTS):
      S1 = 0
      THj = THETC*(j - j0)
      for n1 in range(1, nmax1+1):
          n = n1 - 1
          S1 += ADH[n1-1]*np.cos(n*THj) + BDH[n1-1]*np.sin(n*THj)
      epsIH[j] = S1

  # Layer 6: CME calculation
  R = np.zeros((M1, M1), dtype=complex)
  for i in range(1, M1+1):
      for j in range(1, M1+1):
          if j < i:
              R[i-1, j-1] = np.conj(RH[i-j])
          else:
              R[i-1, j-1] = RH[j-i]
  RI = np.linalg.inv(R)

  a0 = np.sqrt(RI[0, 0])
  a = np.zeros(M1, dtype=complex)
  for n1 in range(1, M1+1):
      a[n1-1] = RI[n1-1, 0]/a0

  P = np.zeros(NPTS)
  diff = np.zeros(NPTS)
  for j in range(NPTS):
      THj = THETC*(j - j0)
      S1 = 0
      for k in range(M+1):
          k1 = k +1
          S1 += a[k1-1]*np.exp(-1j*k*THj)
      P[j] = 1/(np.abs(S1)**2)
      diff[j] = epsIH[j] - P[j] + OFF

  # Layer 8: Reverse direction
  APH = np.zeros(nmax1)
  BPH = np.zeros(nmax1)
  lnPH = np.zeros(nmax1)
  phPH = np.zeros(nmax1)
  for n1 in range(0, nmax1+1):
      n = n1 -1
      S1 = 0
      S2 = 0
      for j in range(NPTS):
          THj = THETC*(j - j0)
          S1 += P[j]*np.cos(n*THj)
          S2 += P[j]*np.sin(n*THj)
      APH[n1-1] = FCON*S1
      BPH[n1-1] = FCON*S2
      lnPH[n1-1] = 0.5*np.log(APH[n1-1]**2 + BPH[n1-1]**2)
      phPH[n1-1] = np.arctan2(S2, S1)
  APH[0] = R[0, 0]
  lnPH[0] = np.log(APH[0])

  # Layer 9: undo Hilbert rotation
  APIF = np.zeros(nmax1)
  BPIF = np.zeros(nmax1)
  for n1 in range(0, nmax1+1):
      APIF[n1-1] = APH[n1-1]*cosH + BPH[n1-1]*sinH
      BPIF[n1-1] = -APH[n1-1]*sinH + BPH[n1-1]*cosH
  APIF[0] = ADH[0]
  BPIF[0] = 0

  # Layer 10: calc filtered IRED and data lineshapes
  epsIF = np.zeros(NPTS)
  epsF = np.zeros(NPTS)
  for j in range(NPTS):
      THj = THETC*(j - j0)
      S1 = 0
      for n1 in range(0, nmax1+1):
          n = n1 -1
          S1 += APIF[n1-1]*np.cos(n*THj) + BPIF[n1-1]*np.sin(n*THj)
      epsIF[j] = S1
      epsF[j] = S1 + c1*THj + c2*THj*THj

  # Layer 11: Output
  return(epsF)