# 📋 Relatório de Normalização de Ontologia
**Arquivo:** `audit-log-session-20260227-011701.json`
## 📊 Sumário Executivo
- **Operação:** Carregamento de Ontologia- **Arquivo:** `energy-domain-ontology.ttl`- **Status:** ✅ success- **Data/Hora:** 2026-02-27T01:17:02.132574
- **Operação:** Carregamento de Ontologia- **Arquivo:** `energy-domain-ontology.ttl`- **Status:** ✅ success- **Data/Hora:** 2026-02-27T01:17:26.533138

- **Operação:** Normalização- **Status:** ⚠️ success- **Modo:** 👁️ Validate-only (sem modificações)- **Total de Issues:** 1831- **Erros:** 260- **Total de Avisos:** 1571- **Correções Propostas (não aplicadas):**  - 🔧 IRIs a corrigir: 63 entidades (746 ocorrências/operações)  - 📝 Identificadores a corrigir: 58 entidades  - 🏷️ PrefLabels a corrigir: 328 (206 entidades)  - 📖 Definitions a corrigir: 293 (195 entidades)  - 📊 Total de triplas a modificar: 1327
### 📋 Tabela V — Métricas de Normalização (Referência Artigo)
| Métrica | Auto-fix desabilitado |
|---------|----------------------|
| Total de issues detectados | 1,831 |
| Erros | 260 |
| Avisos | 1,571 |
| Correções mecânicas propostas (IRI + id.) | 804 operações |
| ↳ IRI: 746 ocorrências (63 entidades) + id.: 58 | |
| Correções semânticas propostas (prefLabel + def.) | 621 triplas |
| Triplas modificadas por correções mecânicas | 0 |
| Correções semânticas aplicadas | 0 (bloqueado) |
- **Data/Hora:** 2026-02-27T01:17:35.139298

### 🔧 Correções de IRI Propostas

> **Formato:** Número sequencial, nome original, nome proposto, e quantas vezes a IRI aparece na ontologia

| # | **Original** | **Proposto** | **Ocorrências** |
|:-:|--------------|---------------|:---------------:|
| 1 | BendingMomentTable_BendingMoment | BendingMomentTableBendingMoment | 12 |
| 2 | BendingMomentTable_Curvature | BendingMomentTableCurvature | 12 |
| 3 | BendMomentVsShearForceTable_BendingMoment | BendMomentVsShearForceTableBendingMoment | 12 |
| 4 | BendMomentVsShearForceTable_Condition | BendMomentVsShearForceTableCondition | 12 |
| 5 | BendMomentVsShearForceTable_ShearForce | BendMomentVsShearForceTableShearForce | 13 |
| 6 | DiffusionTable_DiffusionCoefficient | DiffusionTableDiffusionCoefficient | 12 |
| 7 | DiffusionTable_MoleculeIdentifier | DiffusionTableMoleculeIdentifier | 13 |
| 8 | DiffusionTable_PolymerState | DiffusionTablePolymerState | 13 |
| 9 | DiffusionTable_Temperature | DiffusionTableTemperature | 12 |
| 10 | DomainAnnotation | domainAnnotation | 4 |
| 11 | DomainAuxiliarAnnotation | domainAuxiliarAnnotation | 9 |
| 12 | DomainAuxiliarProperty | domainAuxiliarProperty | 1 |
| 13 | DomainEngineeringAnnotation | domainEngineeringAnnotation | 14 |
| 14 | DomainRelationship | domainRelationship | 2 |
| 15 | DrawingDimensionsTable_DimensionDescription | DrawingDimensionsTableDimensionDescription | 13 |
| 16 | DrawingDimensionsTable_DimensionName | DrawingDimensionsTableDimensionName | 12 |
| 17 | DrawingDimensionsTable_DimensionUnit | DrawingDimensionsTableDimensionUnit | 13 |
| 18 | DrawingDimensionsTable_DimensionValue | DrawingDimensionsTableDimensionValue | 12 |
| 19 | EarlyLeakMaxPressTable_Press | EarlyLeakMaxPressTablePress | 13 |
| 20 | EarlyLeakMaxPressTable_PressIntValStrat | EarlyLeakMaxPressTablePressIntValStrat | 13 |
| 21 | EarlyLeakMaxPressTable_PressValRef | EarlyLeakMaxPressTablePressValRef | 13 |
| 22 | EarlyLeakMaxPressTable_PressValRefMult | EarlyLeakMaxPressTablePressValRefMult | 13 |
| 23 | EarlyLeakMaxPressTable_TensLimit | EarlyLeakMaxPressTableTensLimit | 13 |
| 24 | EarlyLeakMaxPressTable_TensLimitValRef | EarlyLeakMaxPressTableTensLimitValRef | 12 |
| 25 | EarlyLeakNomPressTable_Press | EarlyLeakNomPressTablePress | 13 |
| 26 | EarlyLeakNomPressTable_PressIntValStrat | EarlyLeakNomPressTablePressIntValStrat | 13 |
| 27 | EarlyLeakNomPressTable_PressValRef | EarlyLeakNomPressTablePressValRef | 13 |
| 28 | EarlyLeakNomPressTable_PressValRefMult | EarlyLeakNomPressTablePressValRefMult | 12 |
| 29 | EarlyLeakNomPressTable_TensLimit | EarlyLeakNomPressTableTensLimit | 13 |
| 30 | EarlyLeakNomPressTable_TensLimitValRef | EarlyLeakNomPressTableTensLimitValRef | 12 |
| 31 | EModVsTempTable_ElasticityModulus | EmodVsTempTableElasticityModulus | 13 |
| 32 | EModVsTempTable_Temperature | EmodVsTempTableTemperature | 11 |
| 33 | FrictionCoefficientTighteningTable_CoefficientOfFriction | FrictionCoefficientTighteningTableCoefficientOfFriction | 12 |
| 34 | FrictionCoefficientTighteningTable_TighteningPerTrack | FrictionCoefficientTighteningTableTighteningPerTrack | 12 |
| 35 | InternalIncidentalPressureTable_PositionReference | InternalIncidentalPressureTablePositionReference | 13 |
| 36 | InternalIncidentalPressureTable_Pressure | InternalIncidentalPressureTablePressure | 12 |
| 37 | InternalIncidentalPressureTable_VPosWRTWaterline | InternalIncidentalPressureTableVposWrtwaterline | 13 |
| 38 | LayingMinimumRadiusTable_AbsoluteExternalPressure | LayingMinimumRadiusTableAbsoluteExternalPressure | 12 |
| 39 | LayingMinimumRadiusTable_AbsoluteInternalPressure | LayingMinimumRadiusTableAbsoluteInternalPressure | 12 |
| 40 | LayingMinimumRadiusTable_Compression | LayingMinimumRadiusTableCompression | 13 |
| 41 | LayingMinimumRadiusTable_MinimumAllowableBendingRadius | LayingMinimumRadiusTableMinimumAllowableBendingRadius | 12 |
| 42 | LayingMinimumRadiusTable_SectionSupportedByRigidSupport | LayingMinimumRadiusTableSectionSupportedByRigidSupport | 12 |
| 43 | LayingMinimumRadiusTable_TensileArmourAnnulusCondition | LayingMinimumRadiusTableTensileArmourAnnulusCondition | 13 |
| 44 | MaxDesignAbsIntPresTable_PositionReference | MaxDesignAbsIntPresTablePositionReference | 13 |
| 45 | MaxDesignAbsIntPresTable_Pressure | MaxDesignAbsIntPresTablePressure | 12 |
| 46 | MaxDesignAbsIntPresTable_VPosWRTWaterline | MaxDesignAbsIntPresTableVposWrtwaterline | 13 |
| 47 | MaximumAllowableTensionTable_MaximumAllowableTensile | MaximumAllowableTensionTableMaximumAllowableTensile | 12 |
| 48 | MaximumAllowableTensionTable_PulleyRadius | MaximumAllowableTensionTablePulleyRadius | 12 |
| 49 | MaximumAllowableTensionTable_PulleyVAngle | MaximumAllowableTensionTablePulleyVangle | 12 |
| 50 | MaximumAllowableTighteningTable_AxialLoad | MaximumAllowableTighteningTableAxialLoad | 12 |
| 51 | MaximumAllowableTighteningTable_TighteningPerTrack | MaximumAllowableTighteningTableTighteningPerTrack | 12 |
| 52 | PermeabilityTable_MoleculeIdentifier | PermeabilityTableMoleculeIdentifier | 13 |
| 53 | PermeabilityTable_PermeabilityCoefficient | PermeabilityTablePermeabilityCoefficient | 12 |
| 54 | PermeabilityTable_PolymerState | PermeabilityTablePolymerState | 13 |
| 55 | PermeabilityTable_Temperature | PermeabilityTableTemperature | 12 |
| 56 | Planned_Start_Timestamp | PlannedStartTimestamp | 9 |
| 57 | SolubilityTable_MoleculeIdentifier | SolubilityTableMoleculeIdentifier | 13 |
| 58 | SolubilityTable_PolymerState | SolubilityTablePolymerState | 12 |
| 59 | SolubilityTable_SolubilityCoefficient | SolubilityTableSolubilityCoefficient | 12 |
| 60 | SolubilityTable_Temperature | SolubilityTableTemperature | 12 |
| 61 | StrandsTable_SpareQuantity | StrandsTableSpareQuantity | 12 |
| 62 | StrandsTable_StrandsLength | StrandsTableStrandsLength | 12 |
| 63 | StrandsTable_StrandsQuantity | StrandsTableStrandsQuantity | 12 |

### 📝 Correções de dcterms:identifier Propostas

> **Total:** 58 correções

> **Formato:** Nome da entidade, seguido do valor incorreto (❌) e valor proposto (✅)

**BendingMomentTable_BendingMoment**
- ❌ `BendingMomentTable_BendingMoment`
- ✅ `BendingMomentTableBendingMoment`

**BendingMomentTable_Curvature**
- ❌ `BendingMomentTable_Curvature`
- ✅ `BendingMomentTableCurvature`

**BendMomentVsShearForceTable_BendingMoment**
- ❌ `BendMomentVsShearForceTable_BendingMoment`
- ✅ `BendMomentVsShearForceTableBendingMoment`

**BendMomentVsShearForceTable_Condition**
- ❌ `BendMomentVsShearForceTable_Condition`
- ✅ `BendMomentVsShearForceTableCondition`

**BendMomentVsShearForceTable_ShearForce**
- ❌ `BendMomentVsShearForceTable_ShearForce`
- ✅ `BendMomentVsShearForceTableShearForce`

**DiffusionTable_DiffusionCoefficient**
- ❌ `DiffusionTable_DiffusionCoefficient`
- ✅ `DiffusionTableDiffusionCoefficient`

**DiffusionTable_MoleculeIdentifier**
- ❌ `DiffusionTable_MoleculeIdentifier`
- ✅ `DiffusionTableMoleculeIdentifier`

**DiffusionTable_PolymerState**
- ❌ `DiffusionTable_PolymerState`
- ✅ `DiffusionTablePolymerState`

**DiffusionTable_Temperature**
- ❌ `DiffusionTable_Temperature`
- ✅ `DiffusionTableTemperature`

**DrawingDimensionsTable_DimensionDescription**
- ❌ `DrawingDimensionsTable_DimensionDescription`
- ✅ `DrawingDimensionsTableDimensionDescription`

**DrawingDimensionsTable_DimensionName**
- ❌ `DrawingDimensionsTable_DimensionName`
- ✅ `DrawingDimensionsTableDimensionName`

**DrawingDimensionsTable_DimensionUnit**
- ❌ `DrawingDimensionsTable_DimensionUnit`
- ✅ `DrawingDimensionsTableDimensionUnit`

**DrawingDimensionsTable_DimensionValue**
- ❌ `DrawingDimensionsTable_DimensionValue`
- ✅ `DrawingDimensionsTableDimensionValue`

**EarlyLeakMaxPressTable_Press**
- ❌ `EarlyLeakMaxPressTable_Press`
- ✅ `EarlyLeakMaxPressTablePress`

**EarlyLeakMaxPressTable_PressIntValStrat**
- ❌ `EarlyLeakMaxPressTable_PressIntValStrat`
- ✅ `EarlyLeakMaxPressTablePressIntValStrat`

**EarlyLeakMaxPressTable_PressValRef**
- ❌ `EarlyLeakMaxPressTable_PressValRef`
- ✅ `EarlyLeakMaxPressTablePressValRef`

**EarlyLeakMaxPressTable_PressValRefMult**
- ❌ `EarlyLeakMaxPressTable_PressValRefMult`
- ✅ `EarlyLeakMaxPressTablePressValRefMult`

**EarlyLeakMaxPressTable_TensLimit**
- ❌ `EarlyLeakMaxPressTable_TensLimit`
- ✅ `EarlyLeakMaxPressTableTensLimit`

**EarlyLeakMaxPressTable_TensLimitValRef**
- ❌ `EarlyLeakMaxPressTable_TensLimitValRef`
- ✅ `EarlyLeakMaxPressTableTensLimitValRef`

**EarlyLeakNomPressTable_Press**
- ❌ `EarlyLeakNomPressTable_Press`
- ✅ `EarlyLeakNomPressTablePress`

**EarlyLeakNomPressTable_PressIntValStrat**
- ❌ `EarlyLeakNomPressTable_PressIntValStrat`
- ✅ `EarlyLeakNomPressTablePressIntValStrat`

**EarlyLeakNomPressTable_PressValRef**
- ❌ `EarlyLeakNomPressTable_PressValRef`
- ✅ `EarlyLeakNomPressTablePressValRef`

**EarlyLeakNomPressTable_PressValRefMult**
- ❌ `EarlyLeakNomPressTable_PressValRefMult`
- ✅ `EarlyLeakNomPressTablePressValRefMult`

**EarlyLeakNomPressTable_TensLimit**
- ❌ `EarlyLeakNomPressTable_TensLimit`
- ✅ `EarlyLeakNomPressTableTensLimit`

**EarlyLeakNomPressTable_TensLimitValRef**
- ❌ `EarlyLeakNomPressTable_TensLimitValRef`
- ✅ `EarlyLeakNomPressTableTensLimitValRef`

**EModVsTempTable_ElasticityModulus**
- ❌ `EModVsTempTable_ElasticityModulus`
- ✅ `EmodVsTempTableElasticityModulus`

**EModVsTempTable_Temperature**
- ❌ `EModVsTempTable_Temperature`
- ✅ `EmodVsTempTableTemperature`

**FrictionCoefficientTighteningTable_CoefficientOfFriction**
- ❌ `FrictionCoefficientTighteningTable_CoefficientOfFriction`
- ✅ `FrictionCoefficientTighteningTableCoefficientOfFriction`

**FrictionCoefficientTighteningTable_TighteningPerTrack**
- ❌ `FrictionCoefficientTighteningTable_TighteningPerTrack`
- ✅ `FrictionCoefficientTighteningTableTighteningPerTrack`

**InternalIncidentalPressureTable_PositionReference**
- ❌ `InternalIncidentalPressureTable_PositionReference`
- ✅ `InternalIncidentalPressureTablePositionReference`

**InternalIncidentalPressureTable_Pressure**
- ❌ `InternalIncidentalPressureTable_Pressure`
- ✅ `InternalIncidentalPressureTablePressure`

**InternalIncidentalPressureTable_VPosWRTWaterline**
- ❌ `InternalIncidentalPressureTable_VPosWRTWaterline`
- ✅ `InternalIncidentalPressureTableVposWrtwaterline`

**LayingMinimumRadiusTable_AbsoluteExternalPressure**
- ❌ `LayingMinimumRadiusTable_AbsoluteExternalPressure`
- ✅ `LayingMinimumRadiusTableAbsoluteExternalPressure`

**LayingMinimumRadiusTable_AbsoluteInternalPressure**
- ❌ `LayingMinimumRadiusTable_AbsoluteInternalPressure`
- ✅ `LayingMinimumRadiusTableAbsoluteInternalPressure`

**LayingMinimumRadiusTable_Compression**
- ❌ `LayingMinimumRadiusTable_Compression`
- ✅ `LayingMinimumRadiusTableCompression`

**LayingMinimumRadiusTable_MinimumAllowableBendingRadius**
- ❌ `LayingMinimumRadiusTable_MinimumAllowableBendingRadius`
- ✅ `LayingMinimumRadiusTableMinimumAllowableBendingRadius`

**LayingMinimumRadiusTable_SectionSupportedByRigidSupport**
- ❌ `LayingMinimumRadiusTable_SectionSupportedByRigidSupport`
- ✅ `LayingMinimumRadiusTableSectionSupportedByRigidSupport`

**LayingMinimumRadiusTable_TensileArmourAnnulusCondition**
- ❌ `LayingMinimumRadiusTable_TensileArmourAnnulusCondition`
- ✅ `LayingMinimumRadiusTableTensileArmourAnnulusCondition`

**MaxDesignAbsIntPresTable_PositionReference**
- ❌ `MaxDesignAbsIntPresTable_PositionReference`
- ✅ `MaxDesignAbsIntPresTablePositionReference`

**MaxDesignAbsIntPresTable_Pressure**
- ❌ `MaxDesignAbsIntPresTable_Pressure`
- ✅ `MaxDesignAbsIntPresTablePressure`

**MaxDesignAbsIntPresTable_VPosWRTWaterline**
- ❌ `MaxDesignAbsIntPresTable_VPosWRTWaterline`
- ✅ `MaxDesignAbsIntPresTableVposWrtwaterline`

**MaximumAllowableTensionTable_MaximumAllowableTensile**
- ❌ `MaximumAllowableTensionTable_MaximumAllowableTensile`
- ✅ `MaximumAllowableTensionTableMaximumAllowableTensile`

**MaximumAllowableTensionTable_PulleyRadius**
- ❌ `MaximumAllowableTensionTable_PulleyRadius`
- ✅ `MaximumAllowableTensionTablePulleyRadius`

**MaximumAllowableTensionTable_PulleyVAngle**
- ❌ `MaximumAllowableTensionTable_PulleyVAngle`
- ✅ `MaximumAllowableTensionTablePulleyVangle`

**MaximumAllowableTighteningTable_AxialLoad**
- ❌ `MaximumAllowableTighteningTable_AxialLoad`
- ✅ `MaximumAllowableTighteningTableAxialLoad`

**MaximumAllowableTighteningTable_TighteningPerTrack**
- ❌ `MaximumAllowableTighteningTable_TighteningPerTrack`
- ✅ `MaximumAllowableTighteningTableTighteningPerTrack`

**PermeabilityTable_MoleculeIdentifier**
- ❌ `PermeabilityTable_MoleculeIdentifier`
- ✅ `PermeabilityTableMoleculeIdentifier`

**PermeabilityTable_PermeabilityCoefficient**
- ❌ `PermeabilityTable_PermeabilityCoefficient`
- ✅ `PermeabilityTablePermeabilityCoefficient`

**PermeabilityTable_PolymerState**
- ❌ `PermeabilityTable_PolymerState`
- ✅ `PermeabilityTablePolymerState`

**PermeabilityTable_Temperature**
- ❌ `PermeabilityTable_Temperature`
- ✅ `PermeabilityTableTemperature`

**Planned_Start_Timestamp**
- ❌ `Planned_Start_Timestamp`
- ✅ `PlannedStartTimestamp`

**SolubilityTable_MoleculeIdentifier**
- ❌ `SolubilityTable_MoleculeIdentifier`
- ✅ `SolubilityTableMoleculeIdentifier`

**SolubilityTable_PolymerState**
- ❌ `SolubilityTable_PolymerState`
- ✅ `SolubilityTablePolymerState`

**SolubilityTable_SolubilityCoefficient**
- ❌ `SolubilityTable_SolubilityCoefficient`
- ✅ `SolubilityTableSolubilityCoefficient`

**SolubilityTable_Temperature**
- ❌ `SolubilityTable_Temperature`
- ✅ `SolubilityTableTemperature`

**StrandsTable_SpareQuantity**
- ❌ `StrandsTable_SpareQuantity`
- ✅ `StrandsTableSpareQuantity`

**StrandsTable_StrandsLength**
- ❌ `StrandsTable_StrandsLength`
- ✅ `StrandsTableStrandsLength`

**StrandsTable_StrandsQuantity**
- ❌ `StrandsTable_StrandsQuantity`
- ✅ `StrandsTableStrandsQuantity`


### 🏷️ Correções de skos:prefLabel Propostas

> **Total:** 328 correções

> **Formato:** Nome da entidade, seguido do idioma [en/pt-br], valor incorreto (❌) e valor proposto (✅)

**ActuatedValve**
- [en] ❌ `Externally-actuated valve`
- [en] ✅ `Externally-Actuated Valve`
- [pt-br] ❌ `Válvula atuada externamente`
- [pt-br] ✅ `Válvula Atuada Externamente`

**AssemblyTorque**
- [pt-br] ❌ `Torque de montagem`
- [pt-br] ✅ `Torque de Montagem`

**AuxiliaryModule**
- [en] ❌ `Auxiliary module`
- [en] ✅ `Auxiliary Module`
- [pt-br] ❌ `Módulo auxiliar`
- [pt-br] ✅ `Módulo Auxiliar`

**AxialStiffnessUnderCompressionAtSeaLevel**
- [en] ❌ `Axial Stiffness Under Compression At Sea Level`
- [en] ✅ `Axial Stiffness Under Compression at Sea Level`

**AxialStiffnessUnderTensionAtSeaLevel**
- [en] ❌ `Axial Stiffness Under Tension At Sea Level`
- [en] ✅ `Axial Stiffness Under Tension at Sea Level`

**BendMomentVsShearForceTable_BendingMoment**
- [pt-br] ❌ `Momento de flexão`
- [pt-br] ✅ `Momento de Flexão`

**BendMomentVsShearForceTable_Condition**
- [pt-br] ❌ `Condição do flexível para os dados da curva`
- [pt-br] ✅ `Condição do Flexível para os Dados da Curva`

**BendMomentVsShearForceTableColumn**
- [en] ❌ `Bending moment vs Shear Force Table`
- [en] ✅ `Bending Moment vs Shear Force Table`

**BlockValve**
- [en] ❌ `Block valve`
- [en] ✅ `Block Valve`
- [pt-br] ❌ `Válvula de bloqueio`
- [pt-br] ✅ `Válvula de Bloqueio`

**BOP**
- [en] ❌ `Blowout preventer`
- [en] ✅ `Blowout Preventer`
- [pt-br] ❌ `Blowout preventer`
- [pt-br] ✅ `Blowout Preventer`

**BsddDataDictionary**
- [en] ❌ `BSDD Data Dictionary`
- [en] ✅ `Bsdd Data Dictionary`
- [pt-br] ❌ `Dicionário de Dados BSDD`
- [pt-br] ✅ `Dicionário de Dados Bsdd`

**BuoyancyTank**
- [en] ❌ `Buoyancy tank`
- [en] ✅ `Buoyancy Tank`
- [pt-br] ❌ `Tanque de flutuação`
- [pt-br] ✅ `Tanque de Flutuação`

**CasingHanger**
- [en] ❌ `Casing hanger`
- [en] ✅ `Casing Hanger`
- [pt-br] ❌ `Suspensor de revestimento`
- [pt-br] ✅ `Suspensor de Revestimento`

**ChainSegment**
- [en] ❌ `Chain segment`
- [en] ✅ `Chain Segment`
- [pt-br] ❌ `Tramo de corrente`
- [pt-br] ✅ `Tramo de Corrente`

**ChemicalInjectionUnit**
- [en] ❌ `Chemical injection unit`
- [en] ✅ `Chemical Injection Unit`
- [pt-br] ❌ `Unidade de injeção de químicos`
- [pt-br] ✅ `Unidade de Injeção de Químicos`

**ChokeModule**
- [en] ❌ `Choke module`
- [en] ✅ `Choke Module`
- [pt-br] ❌ `Módulo de choke`
- [pt-br] ✅ `Módulo de Choke`

**ClampInternalDiameter**
- [pt-br] ❌ `Diâmetro interno do clamp`
- [pt-br] ✅ `Diâmetro Interno do Clamp`

**ConnectionModule**
- [en] ❌ `Connection module`
- [en] ✅ `Connection Module`
- [pt-br] ❌ `Módulo de conexão`
- [pt-br] ✅ `Módulo de Conexão`

**CreatorId**
- [en] ❌ `Creator Id`
- [en] ✅ `Creator ID`

**CriticalCurvatureOfSlipping**
- [en] ❌ `Critical Curvature Of Slipping`
- [en] ✅ `Critical Curvature of Slipping`
- [pt-br] ❌ `Curvatura crítica de escorregamento`
- [pt-br] ✅ `Curvatura Crítica de Escorregamento`

**CrossoverModule**
- [en] ❌ `Cross-over module`
- [en] ✅ `Cross-Over Module`
- [pt-br] ❌ `Módulo de cross-over`
- [pt-br] ✅ `Módulo de Cross-Over`

**DeploymentAccessory**
- [en] ❌ `Deployment accessory`
- [en] ✅ `Deployment Accessory`
- [pt-br] ❌ `Acessório de lançamento`
- [pt-br] ✅ `Acessório de Lançamento`

**DiffusionTable_DiffusionCoefficient**
- [pt-br] ❌ `Coeficiente de difusão`
- [pt-br] ✅ `Coeficiente de Difusão`

**DistributionModule**
- [en] ❌ `Distribution module`
- [en] ✅ `Distribution Module`
- [pt-br] ❌ `Módulo de distribuição`
- [pt-br] ✅ `Módulo de Distribuição`

**DragAnchor**
- [en] ❌ `Drag anchor`
- [en] ✅ `Drag Anchor`
- [pt-br] ❌ `Âncora de arrasto`
- [pt-br] ✅ `Âncora de Arrasto`

**DrawingDimensionsTable_DimensionName**
- [pt-br] ❌ `Nome da dimensão`
- [pt-br] ✅ `Nome da Dimensão`

**DrawingDimensionsTable_DimensionValue**
- [pt-br] ❌ `Valor da dimensão`
- [pt-br] ✅ `Valor da Dimensão`

**DynamicUmbilicalSpan**
- [en] ❌ `Dynamic umbilical span`
- [en] ✅ `Dynamic Umbilical Span`
- [pt-br] ❌ `Trecho dinâmico de umbilical`
- [pt-br] ✅ `Trecho Dinâmico de Umbilical`

**ElasticityModulusAt23Degrees**
- [en] ❌ `Elasticity Modulus At 23 Degrees`
- [en] ✅ `Elasticity Modulus at 23 Degrees`

**ElectricalCable**
- [en] ❌ `Electrical cable`
- [en] ✅ `Electrical Cable`
- [pt-br] ❌ `Cabo elétrico`
- [pt-br] ✅ `Cabo Elétrico`

**ElectricalJumper**
- [en] ❌ `Electrical jumper`
- [en] ✅ `Electrical Jumper`
- [pt-br] ❌ `Jumper elétrico`
- [pt-br] ✅ `Jumper Elétrico`

**ElectricalPowerJumper**
- [en] ❌ `Electrical power jumper`
- [en] ✅ `Electrical Power Jumper`
- [pt-br] ❌ `Jumper elétrico de potência`
- [pt-br] ✅ `Jumper Elétrico de Potência`

**ElectronicDevice**
- [en] ❌ `Electronic device`
- [en] ✅ `Electronic Device`
- [pt-br] ❌ `Dispositivo eletrônico`
- [pt-br] ✅ `Dispositivo Eletrônico`

**EndFitting**
- [en] ❌ `End fitting`
- [en] ✅ `End Fitting`

**ErosionalVelocity**
- [pt-br] ❌ `Velocidade erosional`
- [pt-br] ✅ `Velocidade Erosional`

**ExternalDiameter**
- [pt-br] ❌ `Diâmetro externo`
- [pt-br] ✅ `Diâmetro Externo`

**FiberRopeSegment**
- [en] ❌ `Fiber rope segment`
- [en] ✅ `Fiber Rope Segment`
- [pt-br] ❌ `Tramo de cabo de fibra`
- [pt-br] ✅ `Tramo de Cabo de Fibra`

**FlexibleStructure**
- [en] ❌ `FlexibleStructure`
- [en] ✅ `Flexiblestructure`

**FloatingProductionUnit**
- [pt-br] ❌ `Unidade de Produção Flutuante (UEP)`
- [pt-br] ✅ `Unidade de Produção Flutuante (uep)`

**FlowbaseRunningTool**
- [en] ❌ `Flowbase running tool`
- [en] ✅ `Flowbase Running Tool`
- [pt-br] ❌ `Ferramenta de instalação de BAP`
- [pt-br] ✅ `Ferramenta de Instalação de BAP`

**FlowControlEquipment**
- [en] ❌ `Flow control equipment`
- [en] ✅ `Flow Control Equipment`
- [pt-br] ❌ `Equipamento de controle de fluxo`
- [pt-br] ✅ `Equipamento de Controle de Fluxo`

**FlowControlModule**
- [en] ❌ `Flow control module`
- [en] ✅ `Flow Control Module`
- [pt-br] ❌ `Módulo de controle de fluxo`
- [pt-br] ✅ `Módulo de Controle de Fluxo`

**FlowLineMandrel**
- [en] ❌ `Flow line mandrel`
- [en] ✅ `Flow Line Mandrel`
- [pt-br] ❌ `Mandril das linhas de fluxo`
- [pt-br] ✅ `Mandril das Linhas de Fluxo`

**FlowlineSpan**
- [en] ❌ `Flowline span`
- [en] ✅ `Flowline Span`
- [pt-br] ❌ `Trecho flowline`
- [pt-br] ✅ `Trecho Flowline`

**FrictionCoefBetweenPipeAndTensioner**
- [en] ❌ `Friction Coefficient Between Pipe And Tensioner`
- [en] ✅ `Friction Coefficient Between Pipe and Tensioner`

**FrictionCoefficientTighteningTable_CoefficientOfFriction**
- [en] ❌ `Coefficient Of Friction`
- [en] ✅ `Coefficient of Friction`

**FrictionCoefficientTighteningTable_TighteningPerTrack**
- [en] ❌ `Tightening Per Track`
- [en] ✅ `Tightening per Track`
- [pt-br] ❌ `Aperto por lagarta`
- [pt-br] ✅ `Aperto por Lagarta`

**FSHRLowerAssembly**
- [en] ❌ `FSHR lower assembly`
- [en] ✅ `Fshr Lower Assembly`
- [pt-br] ❌ `Estrutura inferior de RHAS`
- [pt-br] ✅ `Estrutura Inferior de Rhas`

**FSHRUpperAssembly**
- [en] ❌ `FSHR upper assembly`
- [en] ✅ `Fshr Upper Assembly`
- [pt-br] ❌ `Estrutura de topo de RHAS`
- [pt-br] ✅ `Estrutura de Topo de Rhas`

**FunctionLine**
- [en] ❌ `Function line`
- [en] ✅ `Function Line`
- [pt-br] ❌ `Linha de função`
- [pt-br] ✅ `Linha de Função`

**GrooveSupportSurfaceDiameter**
- [pt-br] ❌ `Diâmetro da superfície de apoio do acessório`
- [pt-br] ✅ `Diâmetro da Superfície de Apoio do Acessório`

**GrooveSupportSurfaceFilletRadius**
- [pt-br] ❌ `Raio de Chanframento (Superfície de Apoio) do Acessório`
- [pt-br] ✅ `Raio de Chanframento (superfície de Apoio) do Acessório`

**GroutBag**
- [en] ❌ `Grout bag`
- [en] ✅ `Grout Bag`
- [pt-br] ❌ `Grout bag`
- [pt-br] ✅ `Grout Bag`

**GrvCntrPntDstnceFrmTermFlange**
- [en] ❌ `Groove Center Point Distance From Termination Flange`
- [en] ✅ `Groove Center Point Distance from Termination Flange`

**GuideBase**
- [en] ❌ `Guide base`
- [en] ✅ `Guide Base`
- [pt-br] ❌ `Base-guia`
- [pt-br] ✅ `Base-Guia`

**HasModaSensor**
- [pt-br] ❌ `Possui Sensor MODA`
- [pt-br] ✅ `Possui Sensor Moda`

**HasThermalInsulation**
- [pt-br] ❌ `Possui isolamento térmico`
- [pt-br] ✅ `Possui Isolamento Térmico`

**HCM**
- [en] ❌ `Horizontal connection module`
- [en] ✅ `Horizontal Connection Module`
- [pt-br] ❌ `Módulo de conexão horizontal`
- [pt-br] ✅ `Módulo de Conexão Horizontal`

**HPHousing**
- [en] ❌ `High-pressure housing`
- [en] ✅ `High-Pressure Housing`
- [pt-br] ❌ `Alojador de alta pressão`
- [pt-br] ✅ `Alojador de Alta Pressão`

**HubBlockCap**
- [en] ❌ `Hub block cap`
- [en] ✅ `Hub Block Cap`
- [pt-br] ❌ `Capa de bloqueio de hub`
- [pt-br] ✅ `Capa de Bloqueio de Hub`

**HubProtectionCap**
- [en] ❌ `Hub protection cap`
- [en] ✅ `Hub Protection Cap`
- [pt-br] ❌ `Capa de proteção de hub`
- [pt-br] ✅ `Capa de Proteção de Hub`

**HydraulicJumper**
- [en] ❌ `Hydraulic jumper`
- [en] ✅ `Hydraulic Jumper`
- [pt-br] ❌ `Jumper hidráulico`
- [pt-br] ✅ `Jumper Hidráulico`

**HydraulicPowerUnit**
- [en] ❌ `Hydraulic power unit`
- [en] ✅ `Hydraulic Power Unit`
- [pt-br] ❌ `Unidade de potência hidráulica`
- [pt-br] ✅ `Unidade de Potência Hidráulica`

**IdInUnifilarDiagram**
- [en] ❌ `Id In Unifilar Diagram`
- [en] ✅ `ID in Unifilar Diagram`

**IMUX**
- [en] ❌ `IWIS multiplexer`
- [en] ✅ `Iwis Multiplexer`
- [pt-br] ❌ `Multiplexador IWIS`
- [pt-br] ✅ `Multiplexador Iwis`

**InlineT**
- [en] ❌ `Inline tee`
- [en] ✅ `Inline Tee`
- [pt-br] ❌ `'T' em linha`
- [pt-br] ✅ `'t' em Linha`

**InlineValve**
- [en] ❌ `Inline valve`
- [en] ✅ `Inline Valve`
- [pt-br] ❌ `Válvula inline`
- [pt-br] ✅ `Válvula Inline`

**InlineY**
- [en] ❌ `Inline wye`
- [en] ✅ `Inline Wye`
- [pt-br] ❌ `'Y' em linha`
- [pt-br] ✅ `'y' em Linha`

**IntegratedPipe**
- [en] ❌ `Integrated pipe`
- [en] ✅ `Integrated Pipe`
- [pt-br] ❌ `Duto integrado`
- [pt-br] ✅ `Duto Integrado`

**InternalDiameter**
- [pt-br] ❌ `Diâmetro interno`
- [pt-br] ✅ `Diâmetro Interno`

**InternalIncidentalPressureTable_VPosWRTWaterline**
- [en] ❌ `Vertical Position With Respect To Waterline`
- [en] ✅ `Vertical Position with Respect to Waterline`
- [pt-br] ❌ `Posição Vertical em Relação à Linha D'Água`
- [pt-br] ✅ `Posição Vertical em Relação à Linha d'Água`

**InternalVolume**
- [pt-br] ❌ `Volume interno`
- [pt-br] ✅ `Volume Interno`

**IsSpare**
- [pt-br] ❌ `É um sobressalente`
- [pt-br] ✅ `É um Sobressalente`

**ITube**
- [en] ❌ `I-tube`
- [en] ✅ `I-TUBE`
- [pt-br] ❌ `I-tube`
- [pt-br] ✅ `I-TUBE`

**Jumper**
- [en] ❌ `Signal/control jumper`
- [en] ✅ `Signal/control Jumper`
- [pt-br] ❌ `Jumper de controle/sinal`
- [pt-br] ✅ `Jumper de Controle/sinal`

**LayerGeometryInertiaY**
- [pt-br] ❌ `Inércia  Y da Geometria da Camada`
- [pt-br] ✅ `Inércia Y da Geometria da Camada`

**LayerThickness**
- [pt-br] ❌ `Espessura da camada`
- [pt-br] ✅ `Espessura da Camada`

**LayingMinimumRadiusTable_AbsoluteExternalPressure**
- [pt-br] ❌ `Pressão Externa absoluta`
- [pt-br] ✅ `Pressão Externa Absoluta`

**LayingMinimumRadiusTable_AbsoluteInternalPressure**
- [pt-br] ❌ `Pressão interna absoluta`
- [pt-br] ✅ `Pressão Interna Absoluta`

**LayingMinimumRadiusTable_SectionSupportedByRigidSupport**
- [en] ❌ `Section Supported By Rigid Support`
- [en] ✅ `Section Supported by Rigid Support`

**LimpTorsionalStiffnessAtSeaLevel**
- [en] ❌ `Limp Torsional Stiffness At Sea Level`
- [en] ✅ `Limp Torsional Stiffness at Sea Level`

**LineSpan**
- [en] ❌ `Line span`
- [en] ✅ `Line Span`
- [pt-br] ❌ `Trecho de linha`
- [pt-br] ✅ `Trecho de Linha`

**LineTerminationModule**
- [en] ❌ `Line termination module`
- [en] ✅ `Line Termination Module`
- [pt-br] ❌ `Módulo de terminação de linha`
- [pt-br] ✅ `Módulo de Terminação de Linha`

**LogicCap**
- [en] ❌ `Logic cap`
- [en] ✅ `Logic Cap`
- [pt-br] ❌ `Capa lógica`
- [pt-br] ✅ `Capa Lógica`

**LPHousing**
- [en] ❌ `Low-pressure housing`
- [en] ✅ `Low-Pressure Housing`
- [pt-br] ❌ `Alojador de baixa pressão`
- [pt-br] ✅ `Alojador de Baixa Pressão`

**LubricantFrictionFactor**
- [pt-br] ❌ `Fator de atrito do lubrificante`
- [pt-br] ✅ `Fator de Atrito do Lubrificante`

**ManufacturerDefinedMaterialName**
- [pt-br] ❌ `Nome do material conforme designado pelo fabricante do item final`
- [pt-br] ✅ `Nome do Material Conforme Designado pelo Fabricante do Item Final`

**MasterControlStation**
- [en] ❌ `Master control station`
- [en] ✅ `Master Control Station`
- [pt-br] ❌ `Estação de controle mestra`
- [pt-br] ✅ `Estação de Controle Mestra`

**MaterialRequest**
- [pt-br] ❌ `Código da Requisição de Material (RM)`
- [pt-br] ✅ `Código da Requisição de Material (rm)`

**MaterialRequestRev**
- [pt-br] ❌ `Revisão da Requisição de Material (RM)`
- [pt-br] ✅ `Revisão da Requisição de Material (rm)`

**MaterialSupplierName**
- [pt-br] ❌ `Nome da empresa responsável por fornecer o material`
- [pt-br] ✅ `Nome da Empresa Responsável por Fornecer o Material`

**MaxDesignAbsIntPresTable_VPosWRTWaterline**
- [en] ❌ `Vertical Position With Respect To Waterline`
- [en] ✅ `Vertical Position with Respect to Waterline`
- [pt-br] ❌ `Posição Vertical em Relação à Linha D'Água`
- [pt-br] ✅ `Posição Vertical em Relação à Linha d'Água`

**MaxDynamicLoad**
- [en] ❌ `Maximum Dynamic Load (MDL)`
- [en] ✅ `Maximum Dynamic Load (mdl)`
- [pt-br] ❌ `Carga Dinâmica Máxima (MDL)`
- [pt-br] ✅ `Carga Dinâmica Máxima (mdl)`

**MaximumAllowableTensileForStraightLine**
- [en] ❌ `Maximum Allowable Tensile For Straight Line`
- [en] ✅ `Maximum Allowable Tensile for Straight Line`

**MaximumAllowableTighteningTable_TighteningPerTrack**
- [en] ❌ `Tightening Per Track`
- [en] ✅ `Tightening per Track`

**MaximumAmbientTemperature**
- [pt-br] ❌ `Temperatura ambiente máxima`
- [pt-br] ✅ `Temperatura Ambiente Máxima`

**MaximumThermalExchangeCoefficient**
- [en] ❌ `Maximum Thermal Exchange Coefficient (TEC)`
- [en] ✅ `Maximum Thermal Exchange Coefficient (tec)`
- [pt-br] ❌ `Coeficiente Máximo de Troca Térmica (TEC)`
- [pt-br] ✅ `Coeficiente Máximo de Troca Térmica (tec)`

**MetallicTubing**
- [en] ❌ `Metallic tubing`
- [en] ✅ `Metallic Tubing`
- [pt-br] ❌ `Tubulação metálica`
- [pt-br] ✅ `Tubulação Metálica`

**MinimumBendingRadiusForStorage**
- [en] ❌ `Minimum Bending Radius For Storage`
- [en] ✅ `Minimum Bending Radius for Storage`

**MinimumThermalExchangeCoefficient**
- [en] ❌ `Minimum Thermal Exchange Coefficient (TEC)`
- [en] ✅ `Minimum Thermal Exchange Coefficient (tec)`
- [pt-br] ❌ `Coeficiente Mínimo de Troca Térmica (TEC)`
- [pt-br] ✅ `Coeficiente Mínimo de Troca Térmica (tec)`

**ModulusOfElasticity**
- [en] ❌ `Modulus Of Elasticity`
- [en] ✅ `Modulus of Elasticity`
- [pt-br] ❌ `Módulo de elasticidade`
- [pt-br] ✅ `Módulo de Elasticidade`

**NumberOfChokeValves**
- [en] ❌ `Number Of Choke Valves`
- [en] ✅ `Number of Choke Valves`
- [pt-br] ❌ `Número de válvulas de estrangulamento`
- [pt-br] ✅ `Número de Válvulas de Estrangulamento`

**NumberOfRemoteProcessIsolationValves**
- [en] ❌ `Number Of Remote Process Isolation Valves`
- [en] ✅ `Number of Remote Process Isolation Valves`
- [pt-br] ❌ `Número de válvulas de isolamento de processo remoto`
- [pt-br] ✅ `Número de Válvulas de Isolamento de Processo Remoto`

**OffLeakPLevMaxPress**
- [en] ❌ `Offshore Leak Test At Platform Level Maximum Pressure`
- [en] ✅ `Offshore Leak Test at Platform Level Maximum Pressure`

**OffLeakPLevMaxPressValRef**
- [en] ❌ `Offshore Leak Test At Platform Level Maximum Pressure Value Reference`
- [en] ✅ `Offshore Leak Test at Platform Level Maximum Pressure Value Reference`

**OffLeakPLevMaxPressValRefMult**
- [en] ❌ `Offshore Leak Test At Platform Level Maximum Pressure Value Reference Multiplier`
- [en] ✅ `Offshore Leak Test at Platform Level Maximum Pressure Value Reference Multiplier`

**OffLeakPLevNomPress**
- [en] ❌ `Offshore Leak Test At Platform Level Nominal Pressure`
- [en] ✅ `Offshore Leak Test at Platform Level Nominal Pressure`

**OffLeakPLevNomPressValRef**
- [en] ❌ `Offshore Leak Test At Platform Level Nominal Pressure Value Reference`
- [en] ✅ `Offshore Leak Test at Platform Level Nominal Pressure Value Reference`

**OffLeakPLevNomPressValRefMult**
- [en] ❌ `Offshore Leak Test At Platform Level Nominal Pressure Value Reference Multiplier`
- [en] ✅ `Offshore Leak Test at Platform Level Nominal Pressure Value Reference Multiplier`

**OpenReceptacle**
- [en] ❌ `Open receptacle`
- [en] ✅ `Open Receptacle`
- [pt-br] ❌ `Receptáculo aberto`
- [pt-br] ✅ `Receptáculo Aberto`

**OpticalFiberCable**
- [en] ❌ `Optical fiber cable`
- [en] ✅ `Optical Fiber Cable`
- [pt-br] ❌ `Cabo de fibra ótica`
- [pt-br] ✅ `Cabo de Fibra Ótica`

**OuterDiameter**
- [pt-br] ❌ `Diâmetro externo`
- [pt-br] ✅ `Diâmetro Externo`

**PartNumber**
- [pt-br] ❌ `Número da peça do acessório`
- [pt-br] ✅ `Número da Peça do Acessório`

**PipelineSpan**
- [en] ❌ `Pipeline span`
- [en] ✅ `Pipeline Span`
- [pt-br] ❌ `Trecho de duto`
- [pt-br] ✅ `Trecho de Duto`

**PipingSpool**
- [en] ❌ `Piping spool`
- [en] ✅ `Piping Spool`
- [pt-br] ❌ `Trecho de tubulação`
- [pt-br] ✅ `Trecho de Tubulação`

**PlasticHose**
- [pt-br] ❌ `Mangueira plástica`
- [pt-br] ✅ `Mangueira Plástica`

**PoissonRatioAt23Degrees**
- [en] ❌ `Poisson Ratio At 23 Degrees`
- [en] ✅ `Poisson Ratio at 23 Degrees`

**PowerMachine**
- [en] ❌ `Power machine`
- [en] ✅ `Power Machine`
- [pt-br] ❌ `Máquina de potência`
- [pt-br] ✅ `Máquina de Potência`

**PressureComponent**
- [en] ❌ `Pressure-containing component`
- [en] ✅ `Pressure-Containing Component`
- [pt-br] ❌ `Component de contenção de pressão`
- [pt-br] ✅ `Component de Contenção de Pressão`

**PressureEquipment**
- [en] ❌ `Pressure-containing equipment`
- [en] ✅ `Pressure-Containing Equipment`
- [pt-br] ❌ `Equipamentos de contenção de pressão`
- [pt-br] ✅ `Equipamentos de Contenção de Pressão`

**PressureSensor**
- [en] ❌ `Pressure sensor`
- [en] ✅ `Pressure Sensor`
- [pt-br] ❌ `Sensor de pressão`
- [pt-br] ✅ `Sensor de Pressão`

**ProcessingModule**
- [en] ❌ `Processing module`
- [en] ✅ `Processing Module`
- [pt-br] ❌ `Módulo de processamento`
- [pt-br] ✅ `Módulo de Processamento`

**ProjectCode**
- [pt-br] ❌ `Código Identificador único do projeto da operadora da Interligação Submarina`
- [pt-br] ✅ `Código Identificador Único do Projeto da Operadora da Interligação Submarina`

**PumpingModule**
- [en] ❌ `Pumping module`
- [en] ✅ `Pumping Module`
- [pt-br] ❌ `Módulo de bombeamento`
- [pt-br] ✅ `Módulo de Bombeamento`

**QuickDisconnectionTool**
- [en] ❌ `Quick disconnection tool`
- [en] ✅ `Quick Disconnection Tool`
- [pt-br] ❌ `Ferramenta de desconexão rápida`
- [pt-br] ✅ `Ferramenta de Desconexão Rápida`

**ReliefValve**
- [en] ❌ `Relief valve`
- [en] ✅ `Relief Valve`
- [pt-br] ❌ `Válvula de alívio`
- [pt-br] ✅ `Válvula de Alívio`

**RigidJumper**
- [en] ❌ `Rigid jumper`
- [en] ✅ `Rigid Jumper`
- [pt-br] ❌ `Jumper rígido`
- [pt-br] ✅ `Jumper Rígido`

**RiserSpan**
- [en] ❌ `Riser span`
- [en] ✅ `Riser Span`
- [pt-br] ❌ `Trecho riser`
- [pt-br] ✅ `Trecho Riser`

**RiserSupport**
- [en] ❌ `Riser support`
- [en] ✅ `Riser Support`
- [pt-br] ❌ `Suporte de riser`
- [pt-br] ✅ `Suporte de Riser`

**RiserSupportBuoy**
- [en] ❌ `Riser support buoy`
- [en] ✅ `Riser Support Buoy`
- [pt-br] ❌ `Bóia de sustentação de risers`
- [pt-br] ✅ `Bóia de Sustentação de Risers`

**RoboticActuator**
- [en] ❌ `Robotic actuator`
- [en] ✅ `Robotic Actuator`
- [pt-br] ❌ `Atuador robótico`
- [pt-br] ✅ `Atuador Robótico`

**RopeSegment**
- [en] ❌ `Rope segment`
- [en] ✅ `Rope Segment`
- [pt-br] ❌ `Tramo de cabo`
- [pt-br] ✅ `Tramo de Cabo`

**RotatingMachine**
- [en] ❌ `Rotating machine`
- [en] ✅ `Rotating Machine`
- [pt-br] ❌ `Máquina rotativa`
- [pt-br] ✅ `Máquina Rotativa`

**ROVTool**
- [en] ❌ `ROV tool`
- [en] ✅ `ROV Tool`

**RunningTool**
- [en] ❌ `Subsea running tool`
- [en] ✅ `Subsea Running Tool`
- [pt-br] ❌ `Ferramenta submarina de instalação`
- [pt-br] ✅ `Ferramenta Submarina de Instalação`

**RunOfRiver**
- [en] ❌ `Run-of-River Hydropower`
- [en] ✅ `Run-Of-River Hydropower`
- [pt-br] ❌ `Hidrelétrica a Fio d’Água`
- [pt-br] ✅ `Hidrelétrica a Fio D’água`

**RuptDefAlongFibers**
- [pt-br] ❌ `Deformação de Ruptura longitudinalmente às fibras`
- [pt-br] ✅ `Deformação de Ruptura Longitudinalmente às Fibras`

**RuptDefPerpendFibers**
- [en] ❌ `Rupture Deformation Perpendicular To Fibers`
- [en] ✅ `Rupture Deformation Perpendicular to Fibers`
- [pt-br] ❌ `Deformação de Ruptura perpendicularmente às fibras`
- [pt-br] ✅ `Deformação de Ruptura Perpendicularmente às Fibras`

**SandDetector**
- [en] ❌ `Sand detector`
- [en] ✅ `Sand Detector`
- [pt-br] ❌ `Detector de areia`
- [pt-br] ✅ `Detector de Areia`

**SCM**
- [en] ❌ `Subsea control module`
- [en] ✅ `Subsea Control Module`
- [pt-br] ❌ `Módulo de controle submarino`
- [pt-br] ✅ `Módulo de Controle Submarino`

**SCMMB**
- [en] ❌ `SCM mounting base`
- [en] ✅ `SCM Mounting Base`
- [pt-br] ❌ `Base de montagem de SCM`
- [pt-br] ✅ `Base de Montagem de SCM`

**SCMRunningTool**
- [en] ❌ `SCM running tool`
- [en] ✅ `SCM Running Tool`
- [pt-br] ❌ `Ferramenta de instalação de SCM`
- [pt-br] ✅ `Ferramenta de Instalação de SCM`

**SDU**
- [en] ❌ `Subsea distribution unit`
- [en] ✅ `Subsea Distribution Unit`
- [pt-br] ❌ `Unidade de distribuição submarina`
- [pt-br] ✅ `Unidade de Distribuição Submarina`

**SEM**
- [en] ❌ `Subsea electronic module`
- [en] ✅ `Subsea Electronic Module`
- [pt-br] ❌ `Módulo eletrônico submarino`
- [pt-br] ✅ `Módulo Eletrônico Submarino`

**SeparatorVessel**
- [en] ❌ `Seaparator vessel`
- [en] ✅ `Seaparator Vessel`
- [pt-br] ❌ `Vaso separador`
- [pt-br] ✅ `Vaso Separador`

**ShackleInnerDiameter**
- [pt-br] ❌ `Diâmetro interno da furação do olhal`
- [pt-br] ✅ `Diâmetro Interno da Furação do Olhal`

**ShackleOuterDiameter**
- [pt-br] ❌ `Diâmetro externo do olhal`
- [pt-br] ✅ `Diâmetro Externo do Olhal`

**ShackleThickness**
- [pt-br] ❌ `Espessura do olhal`
- [pt-br] ✅ `Espessura do Olhal`

**ShearableRiserJoint**
- [en] ❌ `Shearable riser joint`
- [en] ✅ `Shearable Riser Joint`
- [pt-br] ❌ `Junta riser cisalhável`
- [pt-br] ✅ `Junta Riser Cisalhável`

**SolubilityCurveAttribute**
- [en] ❌ `Solubility Table (Specific for Polymeric Materials)`
- [en] ✅ `Solubility Table (specific for Polymeric Materials)`
- [pt-br] ❌ `Tabela de Solubilidade (Específica para Materiais Poliméricos)`
- [pt-br] ✅ `Tabela de Solubilidade (específica para Materiais Poliméricos)`

**SolubilityTable_SolubilityCoefficient**
- [pt-br] ❌ `Coeficiente de solubilidade`
- [pt-br] ✅ `Coeficiente de Solubilidade`

**SpliceBox**
- [en] ❌ `Splice box`
- [en] ✅ `Splice Box`
- [pt-br] ❌ `Caixa de emenda`
- [pt-br] ✅ `Caixa de Emenda`

**StaticUmbilicalSpan**
- [en] ❌ `Static umbilical span`
- [en] ✅ `Static Umbilical Span`
- [pt-br] ❌ `Trecho estático de umbilical`
- [pt-br] ✅ `Trecho Estático de Umbilical`

**StiffTorsionalStiffnessAtSeaLevel**
- [en] ❌ `Stiff Torsional Stiffness At Sea Level`
- [en] ✅ `Stiff Torsional Stiffness at Sea Level`

**StorageAccessory**
- [en] ❌ `Storage/transportation accessory`
- [en] ✅ `Storage/transportation Accessory`
- [pt-br] ❌ `Acessório de armazenamento/transporte`
- [pt-br] ✅ `Acessório de Armazenamento/transporte`

**StorageBox**
- [en] ❌ `Storage box`
- [en] ✅ `Storage Box`
- [pt-br] ❌ `Caixa de armazenamento`
- [pt-br] ✅ `Caixa de Armazenamento`

**StorageSkid**
- [en] ❌ `Storage skid`
- [en] ✅ `Storage Skid`
- [pt-br] ❌ `Skid de armazenamento`
- [pt-br] ✅ `Skid de Armazenamento`

**StorageSpool**
- [en] ❌ `Storage spool`
- [en] ✅ `Storage Spool`
- [pt-br] ❌ `Carretel de armazenamento`
- [pt-br] ✅ `Carretel de Armazenamento`

**StressAtDesignPressure**
- [en] ❌ `Stress At Design Pressure`
- [en] ✅ `Stress at Design Pressure`
- [pt-br] ❌ `Tensão na pressão de projeto`
- [pt-br] ✅ `Tensão na Pressão de Projeto`

**StrIntOffPLevMaxPress**
- [en] ❌ `Structural Integrity Offshore Leak Test At Platform Level Maximum Pressure`
- [en] ✅ `Structural Integrity Offshore Leak Test at Platform Level Maximum Pressure`

**StrIntOffPLevMaxPressValRef**
- [en] ❌ `Structural Integrity Offshore Leak Test At Platform Level Maximum Pressure Value Reference`
- [en] ✅ `Structural Integrity Offshore Leak Test at Platform Level Maximum Pressure Value Reference`

**StrIntOffPLevMaxPressValRefMult**
- [en] ❌ `Structural Integrity Offshore Leak Test At Platform Level Maximum Pressure Value Reference Multiplier`
- [en] ✅ `Structural Integrity Offshore Leak Test at Platform Level Maximum Pressure Value Reference Multiplier`

**StrIntOffPLevNomPress**
- [en] ❌ `Structural Integrity Offshore Leak Test At Platform Level Nominal Pressure`
- [en] ✅ `Structural Integrity Offshore Leak Test at Platform Level Nominal Pressure`

**StrIntOffPLevNomPressValRef**
- [en] ❌ `Structural Integrity Offshore Leak Test At Platform Level Nominal Pressure Value Reference`
- [en] ✅ `Structural Integrity Offshore Leak Test at Platform Level Nominal Pressure Value Reference`

**StrIntOffPLevNomPressValRefMult**
- [en] ❌ `Structural Integrity Offshore Leak Test At Platform Level Nominal Pressure Value Reference Multiplier`
- [en] ✅ `Structural Integrity Offshore Leak Test at Platform Level Nominal Pressure Value Reference Multiplier`

**StrIntOnNoTensMaxPress**
- [en] ❌ `Structural Integrity Onboard With No Tension Maximum Pressure`
- [en] ✅ `Structural Integrity Onboard with No Tension Maximum Pressure`

**StrIntOnNoTensMaxPressValRef**
- [en] ❌ `Structural Integrity Onboard With No Tension Maximum Pressure Value Reference`
- [en] ✅ `Structural Integrity Onboard with No Tension Maximum Pressure Value Reference`

**StrIntOnNoTensMaxPressValRefMult**
- [en] ❌ `Structural Integrity Onboard With No Tension Maximum Pressure Value Reference Multiplier`
- [en] ✅ `Structural Integrity Onboard with No Tension Maximum Pressure Value Reference Multiplier`

**StrIntOnNoTensNomPress**
- [en] ❌ `Structural Integrity Onboard With No Tension Nominal Pressure`
- [en] ✅ `Structural Integrity Onboard with No Tension Nominal Pressure`

**StrIntOnNoTensNomPressValRef**
- [en] ❌ `Structural Integrity Onboard With No Tension Nominal Pressure Value Reference`
- [en] ✅ `Structural Integrity Onboard with No Tension Nominal Pressure Value Reference`

**StrIntOnNoTensNomPressValRefMult**
- [en] ❌ `Structural Integrity Onboard With No Tension Nominal Pressure Value Reference Multiplier`
- [en] ✅ `Structural Integrity Onboard with No Tension Nominal Pressure Value Reference Multiplier`

**StructureCode**
- [pt-br] ❌ `Código da estrutura`
- [pt-br] ✅ `Código da Estrutura`

**SubProjectId**
- [en] ❌ `Sub Project Id`
- [en] ✅ `Sub Project ID`
- [pt-br] ❌ `Id do Subprojeto`
- [pt-br] ✅ `ID do Subprojeto`

**SuctionPile**
- [en] ❌ `Suction pile`
- [en] ✅ `Suction Pile`
- [pt-br] ❌ `Estaca de sucção`
- [pt-br] ✅ `Estaca de Sucção`

**SupplierProvidedMaterialName**
- [pt-br] ❌ `Nome do material conforme designado pelo fornecedor original do material`
- [pt-br] ✅ `Nome do Material Conforme Designado pelo Fornecedor Original do Material`

**SupportRegion**
- [pt-br] ❌ `Região de suporte no Modelo`
- [pt-br] ✅ `Região de Suporte no Modelo`

**TapesQuantity**
- [pt-br] ❌ `Quantidade de fitas`
- [pt-br] ✅ `Quantidade de Fitas`

**TemperatureSensor**
- [en] ❌ `Temperature sensor`
- [en] ✅ `Temperature Sensor`
- [pt-br] ❌ `Sensor de temperatura`
- [pt-br] ✅ `Sensor de Temperatura`

**TensileArmourFreeAnnulusVolume**
- [pt-br] ❌ `Volume livre do anular das armaduras de tração`
- [pt-br] ✅ `Volume Livre do Anular das Armaduras de Tração`

**TestBase**
- [en] ❌ `Test base`
- [en] ✅ `Test Base`
- [pt-br] ❌ `Base de teste`
- [pt-br] ✅ `Base de Teste`

**TestEquipment**
- [en] ❌ `Test equipment`
- [en] ✅ `Test Equipment`
- [pt-br] ❌ `Equipamento de teste`
- [pt-br] ✅ `Equipamento de Teste`

**ThreadsPerInch**
- [en] ❌ `Threads Per Inch`
- [en] ✅ `Threads per Inch`

**TieIn**
- [en] ❌ `Tie-in`
- [en] ✅ `Tie-In`
- [pt-br] ❌ `Tie-in`
- [pt-br] ✅ `Tie-In`

**TieInEquipment**
- [en] ❌ `Tie-in equipment`
- [en] ✅ `Tie-In Equipment`
- [pt-br] ❌ `Equipamento de interligação`
- [pt-br] ✅ `Equipamento de Interligação`

**TorpedoPile**
- [en] ❌ `Torpedo pile`
- [en] ✅ `Torpedo Pile`
- [pt-br] ❌ `Estaca-torpedo`
- [pt-br] ✅ `Estaca-Torpedo`

**TPT**
- [en] ❌ `Pressure and temperature sensor`
- [en] ✅ `Pressure and Temperature Sensor`
- [pt-br] ❌ `Sensor de pressão e temperatura`
- [pt-br] ✅ `Sensor de Pressão e Temperatura`

**TreeRunningTool**
- [en] ❌ `Wet Christmas tree running tool`
- [en] ✅ `Wet Christmas Tree Running Tool`
- [pt-br] ❌ `Ferramenta de instalação de ANM`
- [pt-br] ✅ `Ferramenta de Instalação de Anm`

**TrianglePlate**
- [en] ❌ `Triangle plate`
- [en] ✅ `Triangle Plate`
- [pt-br] ❌ `Placa triangular`
- [pt-br] ✅ `Placa Triangular`

**TubingHanger**
- [en] ❌ `Tubing hanger`
- [en] ✅ `Tubing Hanger`
- [pt-br] ❌ `Suspensor de coluna`
- [pt-br] ✅ `Suspensor de Coluna`

**TubingHangerRunningTool**
- [en] ❌ `Tubing hanger running tool`
- [en] ✅ `Tubing Hanger Running Tool`
- [pt-br] ❌ `Ferramenta de instalação de TH`
- [pt-br] ✅ `Ferramenta de Instalação de TH`

**UltTensStrAlongFibers**
- [pt-br] ❌ `Tensão máxima de tração longitudinalmente às fibras`
- [pt-br] ✅ `Tensão Máxima de Tração Longitudinalmente às Fibras`

**UltTensStrPerpendFibers**
- [en] ❌ `Ultimate Tensile Strength Perpendicular To Fibers`
- [en] ✅ `Ultimate Tensile Strength Perpendicular to Fibers`
- [pt-br] ❌ `Tensão máxima de tração perpendicularmente às fibras`
- [pt-br] ✅ `Tensão Máxima de Tração Perpendicularmente às Fibras`

**UmbilicalComponent**
- [en] ❌ `Umbilical component`
- [en] ✅ `Umbilical Component`
- [pt-br] ❌ `Componente de umbilical`
- [pt-br] ✅ `Componente de Umbilical`

**UmbilicalLocation**
- [en] ❌ `Umbilical location`
- [en] ✅ `Umbilical Location`
- [pt-br] ❌ `Local de umbilical`
- [pt-br] ✅ `Local de Umbilical`

**UmbilicalSpan**
- [en] ❌ `Umbilical span`
- [en] ✅ `Umbilical Span`
- [pt-br] ❌ `Trecho de umbilical`
- [pt-br] ✅ `Trecho de Umbilical`

**UpperItubeDiameter**
- [en] ❌ `Upper I-tube Diameter`
- [en] ✅ `Upper I-TUBE Diameter`
- [pt-br] ❌ `Diâmetro do I-TUBE superior`
- [pt-br] ✅ `Diâmetro do I-TUBE Superior`

**UTA**
- [en] ❌ `Umbilical termination assembly`
- [en] ✅ `Umbilical Termination Assembly`
- [pt-br] ❌ `Conjunto de terminação de umbilical`
- [pt-br] ✅ `Conjunto de Terminação de Umbilical`

**UTM**
- [en] ❌ `Umbilical termination module`
- [en] ✅ `Umbilical Termination Module`
- [pt-br] ❌ `Módulo de terminação de umbilical`
- [pt-br] ✅ `Módulo de Terminação de Umbilical`

**VCM**
- [en] ❌ `Vertical connection module`
- [en] ✅ `Vertical Connection Module`
- [pt-br] ❌ `Módulo de conexão vertical`
- [pt-br] ✅ `Módulo de Conexão Vertical`

**WasteToEnergy**
- [pt-br] ❌ `Energia a partir de Resíduos`
- [pt-br] ✅ `Energia a Partir de Resíduos`

**WearBushingRunningTool**
- [en] ❌ `Wear bushing running tool`
- [en] ✅ `Wear Bushing Running Tool`
- [pt-br] ❌ `Ferramenta de instalação de BD`
- [pt-br] ✅ `Ferramenta de Instalação de Bd`

**Wellhead**
- [pt-br] ❌ `Cabeça de poço`
- [pt-br] ✅ `Cabeça de Poço`

**WetChristmasTree**
- [en] ❌ `Wet Christmas tree`
- [en] ✅ `Wet Christmas Tree`
- [pt-br] ❌ `Árvore de Natal molhada`
- [pt-br] ✅ `Árvore de Natal Molhada`

**WireRopeQuantity**
- [pt-br] ❌ `Quantidade de cordas de Aço`
- [pt-br] ✅ `Quantidade de Cordas de Aço`

**WireRopeSegment**
- [en] ❌ `Wire rope segment`
- [en] ✅ `Wire Rope Segment`
- [pt-br] ❌ `Tramo de cabo de aço`
- [pt-br] ✅ `Tramo de Cabo de Aço`

**WorkingLoadLimit**
- [en] ❌ `Working Load Limit (WLL)`
- [en] ✅ `Working Load Limit (wll)`


### 📖 Correções de skos:definition Propostas
| **Entidade** | **Idioma** | **Correção** |
|--------------|------------|---------------|
| `Accessory` | `en` | Ponto final adicionado |
| `Accessory` | `pt-br` | Ponto final adicionado |
| `ActuatedEquipment` | `en` | Ponto final adicionado |
| `ActuatedEquipment` | `pt-br` | Ponto final adicionado |
| `ActuatedValve` | `en` | Ponto final adicionado |
| `ActuatedValve` | `pt-br` | Ponto final adicionado |
| `Anchor` | `en` | Ponto final adicionado |
| `Anchor` | `pt-br` | Ponto final adicionado |
| `appliesTo` | `en` | Ponto final adicionado |
| `appliesTo` | `pt-br` | Ponto final adicionado |
| `ArmorPot` | `en` | Ponto final adicionado |
| `ArmorPot` | `pt-br` | Ponto final adicionado |
| `Asset` | `pt-br` | Ponto final adicionado |
| `AttributeDomainCategory` | `en` | Ponto final adicionado |
| `AttributeDomainCategory` | `pt-br` | Ponto final adicionado |
| `AttributeScope` | `en` | Ponto final adicionado |
| `AttributeScope` | `pt-br` | Ponto final adicionado |
| `AuxiliaryModule` | `en` | Ponto final adicionado |
| `AuxiliaryModule` | `pt-br` | Ponto final adicionado |
| `AxialStiffnessUnderCompressionAtSeaLevel` | `pt-br` | Ponto final adicionado |
| `BatchLevelAttribute` | `en` | Ponto final adicionado |
| `BatchLevelAttribute` | `pt-br` | Ponto final adicionado |
| `BendMomentVsShearForceTable_ShearForce` | `pt-br` | Ponto final adicionado |
| `BlockValve` | `en` | Ponto final adicionado |
| `BlockValve` | `pt-br` | Ponto final adicionado |
| `CalculatedValue` | `en` | Ponto final adicionado |
| `CalculatedValue` | `pt-br` | Ponto final adicionado |
| `CarcassLayer` | `pt-br` | Ponto final adicionado |
| `CheckValve` | `en` | Ponto final adicionado |
| `CheckValve` | `pt-br` | Ponto final adicionado |
| `ChemicalInjectionUnit` | `en` | Ponto final adicionado |
| `ChemicalInjectionUnit` | `pt-br` | Ponto final adicionado |
| `ChokeModule` | `en` | Ponto final adicionado |
| `ChokeModule` | `pt-br` | Ponto final adicionado |
| `ChokeValve` | `en` | Ponto final adicionado |
| `ChokeValve` | `pt-br` | Ponto final adicionado |
| `ClampInternalDiameter` | `en` | Ponto final adicionado |
| `Component` | `pt-br` | Ponto final adicionado |
| `ComponentDevice` | `en` | Ponto final adicionado |
| `ComponentDevice` | `pt-br` | Ponto final adicionado |
| `ConnectionModule` | `en` | Ponto final adicionado |
| `ConnectionModule` | `pt-br` | Ponto final adicionado |
| `CrossoverModule` | `en` | Ponto final adicionado |
| `CrossoverModule` | `pt-br` | Ponto final adicionado |
| `DeclaredValue` | `en` | Ponto final adicionado |
| `DeclaredValue` | `pt-br` | Ponto final adicionado |
| `DiffusionTable_MoleculeIdentifier` | `pt-br` | Ponto final adicionado |
| `DiffusionTable_PolymerState` | `pt-br` | Ponto final adicionado |
| `DiffusionTableColumn` | `pt-br` | Ponto final adicionado |
| `DimensionalAttribute` | `en` | Ponto final adicionado |
| `DimensionalAttribute` | `pt-br` | Ponto final adicionado |
| `DimensioningCriteria` | `pt-br` | Ponto final adicionado |
| `DistributionModule` | `en` | Ponto final adicionado |
| `DrawingDimensionsTable_DimensionDescription` | `pt-br` | Ponto final adicionado |
| `DynamicUmbilicalSpan` | `en` | Ponto final adicionado |
| `DynamicUmbilicalSpan` | `pt-br` | Ponto final adicionado |
| `EarlyLeakMaxPressTable_Press` | `pt-br` | Ponto final adicionado |
| `EarlyLeakMaxPressTable_PressIntValStrat` | `pt-br` | Ponto final adicionado |
| `EarlyLeakMaxPressTable_PressValRef` | `pt-br` | Ponto final adicionado |
| `EarlyLeakMaxPressTable_PressValRefMult` | `pt-br` | Ponto final adicionado |
| `EarlyLeakMaxPressTable_TensLimit` | `pt-br` | Ponto final adicionado |
| `EarlyLeakNomPressTable_Press` | `pt-br` | Ponto final adicionado |
| `EarlyLeakNomPressTable_PressIntValStrat` | `pt-br` | Ponto final adicionado |
| `EarlyLeakNomPressTable_PressValRef` | `pt-br` | Ponto final adicionado |
| `EarlyLeakNomPressTable_TensLimit` | `pt-br` | Ponto final adicionado |
| `ElasticityModulusAt23Degrees` | `pt-br` | Ponto final adicionado |
| `ElectricalJumper` | `en` | Ponto final adicionado |
| `ElectricalJumper` | `pt-br` | Ponto final adicionado |
| `EModVsTempTable_ElasticityModulus` | `pt-br` | Ponto final adicionado |
| `Equipment` | `en` | Ponto final adicionado |
| `Equipment` | `pt-br` | Ponto final adicionado |
| `EquipmentLocation` | `pt-br` | Ponto final adicionado |
| `ExecutiveProjectRevision` | `pt-br` | Ponto final adicionado |
| `FatMaxPress` | `pt-br` | Ponto final adicionado |
| `FatMaxPressValRef` | `pt-br` | Ponto final adicionado |
| `FatNomPress` | `pt-br` | Ponto final adicionado |
| `FatNomPressValRef` | `pt-br` | Ponto final adicionado |
| `FinancialAttribute` | `en` | Ponto final adicionado |
| `FinancialAttribute` | `pt-br` | Ponto final adicionado |
| `FlowConnector` | `en` | Ponto final adicionado |
| `FlowConnector` | `pt-br` | Ponto final adicionado |
| `FlowControlEquipment` | `en` | Ponto final adicionado |
| `FlowControlEquipment` | `pt-br` | Ponto final adicionado |
| `FlowControlModule` | `en` | Ponto final adicionado |
| `FlowControlModule` | `pt-br` | Ponto final adicionado |
| `FlowLineMandrel` | `en` | Ponto final adicionado |
| `FlowLineMandrel` | `pt-br` | Ponto final adicionado |
| `FlowlineSpan` | `en` | Ponto final adicionado |
| `FlowlineSpan` | `pt-br` | Ponto final adicionado |
| `FunctionalAttribute` | `en` | Ponto final adicionado |
| `FunctionalAttribute` | `pt-br` | Ponto final adicionado |
| `GroovePoint` | `pt-br` | Ponto final adicionado |
| `GrooveSupportSurfaceFilletRadius` | `pt-br` | Ponto final adicionado |
| `GrvCntrPntDstnceFrmTermFlange` | `en` | Ponto final adicionado |
| `HangOffCollar` | `pt-br` | Ponto final adicionado |
| `hasAttribute` | `en` | Ponto final adicionado |
| `hasAttribute` | `pt-br` | Ponto final adicionado |
| `hasAttributeCategory` | `en` | Ponto final adicionado |
| `hasAttributeCategory` | `pt-br` | Ponto final adicionado |
| `hasAttributeGroup` | `en` | Ponto final adicionado |
| `hasAttributeGroup` | `pt-br` | Ponto final adicionado |
| `hasAttributeScope` | `en` | Ponto final adicionado |
| `hasAttributeScope` | `pt-br` | Ponto final adicionado |
| `hasDiscipline` | `en` | Ponto final adicionado |
| `hasDiscipline` | `pt-br` | Ponto final adicionado |
| `hasDomain` | `en` | Ponto final adicionado |
| `hasDomain` | `pt-br` | Ponto final adicionado |
| `hasLifecycleCreationPhase` | `en` | Ponto final adicionado |
| `hasLifecycleCreationPhase` | `pt-br` | Ponto final adicionado |
| `hasLifecycleUsagePhase` | `en` | Ponto final adicionado |
| `hasLifecycleUsagePhase` | `pt-br` | Ponto final adicionado |
| `hasLocationType` | `en` | Ponto final adicionado |
| `hasLocationType` | `pt-br` | Ponto final adicionado |
| `hasSubDomain` | `en` | Ponto final adicionado |
| `hasSubDomain` | `pt-br` | Ponto final adicionado |
| `hasValueCardinality` | `en` | Ponto final adicionado |
| `hasValueCardinality` | `pt-br` | Ponto final adicionado |
| `HCRHose` | `en` | Ponto final adicionado |
| `HistoricalAttribute` | `en` | Ponto final adicionado |
| `HistoricalAttribute` | `pt-br` | Ponto final adicionado |
| `Hub` | `en` | Ponto final adicionado |
| `Hub` | `pt-br` | Ponto final adicionado |
| `HubBlockCap` | `en` | Ponto final adicionado |
| `HubBlockCap` | `pt-br` | Ponto final adicionado |
| `HubProtectionCap` | `en` | Ponto final adicionado |
| `HubProtectionCap` | `pt-br` | Ponto final adicionado |
| `HydraulicPowerUnit` | `en` | Ponto final adicionado |
| `HydraulicPowerUnit` | `pt-br` | Ponto final adicionado |
| `HydrostaticCollapseAbsPressDry` | `pt-br` | Ponto final adicionado |
| `IdentificationAttribute` | `en` | Ponto final adicionado |
| `IdentificationAttribute` | `pt-br` | Ponto final adicionado |
| `ifc_equivalentClass` | `en` | Ponto final adicionado |
| `ifc_equivalentClass` | `pt-br` | Ponto final adicionado |
| `ifc_objectType` | `en` | Ponto final adicionado |
| `ifc_objectType` | `pt-br` | Ponto final adicionado |
| `ifc_predefinedType` | `en` | Ponto final adicionado |
| `ifc_predefinedType` | `pt-br` | Ponto final adicionado |
| `ImportedValue` | `en` | Ponto final adicionado |
| `ImportedValue` | `pt-br` | Ponto final adicionado |
| `IMUX` | `en` | Ponto final adicionado |
| `IMUX` | `pt-br` | Ponto final adicionado |
| `InlineT` | `en` | Ponto final adicionado |
| `InlineT` | `pt-br` | Ponto final adicionado |
| `InlineY` | `en` | Ponto final adicionado |
| `InlineY` | `pt-br` | Ponto final adicionado |
| `InstanceLevelAttribute` | `en` | Ponto final adicionado |
| `InstanceLevelAttribute` | `pt-br` | Ponto final adicionado |
| `InternalIncidentalPressureTable_PositionReference` | `pt-br` | Ponto final adicionado |
| `Jumper` | `en` | Ponto final adicionado |
| `Jumper` | `pt-br` | Ponto final adicionado |
| `LayerAnnular` | `pt-br` | Ponto final adicionado |
| `LayerAnnularType` | `pt-br` | Ponto final adicionado |
| `LayerContinuity` | `pt-br` | Ponto final adicionado |
| `LayingMinimumRadiusTable_TensileArmourAnnulusCondition` | `pt-br` | Ponto final adicionado |
| `LimpTorsionalStiffnessAtSeaLevel` | `pt-br` | Ponto final adicionado |
| `LinearLocation` | `pt-br` | Ponto final adicionado |
| `LinearObject` | `pt-br` | Ponto final adicionado |
| `LineSpan` | `en` | Ponto final adicionado |
| `LineSpan` | `pt-br` | Ponto final adicionado |
| `LineTermination` | `pt-br` | Ponto final adicionado |
| `Location` | `pt-br` | Ponto final adicionado |
| `LongTermFloatDensity` | `pt-br` | Ponto final adicionado |
| `Manifold` | `en` | Ponto final adicionado |
| `Manifold` | `pt-br` | Ponto final adicionado |
| `MasterControlStation` | `en` | Ponto final adicionado |
| `MasterControlStation` | `pt-br` | Ponto final adicionado |
| `Mattress` | `en` | Ponto final adicionado |
| `Mattress` | `pt-br` | Ponto final adicionado |
| `MaxDesignAbsIntPresTable_PositionReference` | `pt-br` | Ponto final adicionado |
| `MaxPermissibleDeformationDynamic` | `pt-br` | Ponto final adicionado |
| `MaxPermissibleDeformationStatic` | `pt-br` | Ponto final adicionado |
| `MeasuredValue` | `en` | Ponto final adicionado |
| `MeasuredValue` | `pt-br` | Ponto final adicionado |
| `MetallicStrandLength` | `en` | Ponto final adicionado |
| `MinimumTemperature` | `en` | Ponto final adicionado |
| `NumberOfChokeValves` | `en` | Ponto final adicionado |
| `NumberOfChokeValves` | `pt-br` | Ponto final adicionado |
| `NumberOfRemoteProcessIsolationValves` | `en` | Ponto final adicionado |
| `NumberOfRemoteProcessIsolationValves` | `pt-br` | Ponto final adicionado |
| `OffLeakPLevMaxPress` | `pt-br` | Ponto final adicionado |
| `OffLeakPLevMaxPressValRef` | `pt-br` | Ponto final adicionado |
| `OffLeakPLevNomPress` | `pt-br` | Ponto final adicionado |
| `OffLeakPLevNomPressValRef` | `pt-br` | Ponto final adicionado |
| `PerformanceAttribute` | `en` | Ponto final adicionado |
| `PerformanceAttribute` | `pt-br` | Ponto final adicionado |
| `PermeabilityCurveAttribute` | `pt-br` | Ponto final adicionado |
| `PermeabilityTable_MoleculeIdentifier` | `pt-br` | Ponto final adicionado |
| `PermeabilityTable_PolymerState` | `pt-br` | Ponto final adicionado |
| `PhysicalConnection` | `pt-br` | Ponto final adicionado |
| `PhysicalPropertyAttribute` | `en` | Ponto final adicionado |
| `PhysicalPropertyAttribute` | `pt-br` | Ponto final adicionado |
| `Piggable` | `en` | Ponto final adicionado |
| `Piggable` | `pt-br` | Ponto final adicionado |
| `PipelineSpan` | `en` | Ponto final adicionado |
| `PipelineSpan` | `pt-br` | Ponto final adicionado |
| `PipeSectionApplication` | `pt-br` | Ponto final adicionado |
| `PipeSegment` | `pt-br` | Ponto final adicionado |
| `PipingSpool` | `en` | Ponto final adicionado |
| `PipingSpool` | `pt-br` | Ponto final adicionado |
| `PLEM` | `en` | Ponto final adicionado |
| `PLEM` | `pt-br` | Ponto final adicionado |
| `PLET` | `en` | Ponto final adicionado |
| `PLET` | `pt-br` | Ponto final adicionado |
| `PointLocation` | `pt-br` | Ponto final adicionado |
| `PoissonRatioAt23Degrees` | `pt-br` | Ponto final adicionado |
| `PowerMachine` | `en` | Ponto final adicionado |
| `PowerMachine` | `pt-br` | Ponto final adicionado |
| `PressureEquipment` | `en` | Ponto final adicionado |
| `PressureEquipment` | `pt-br` | Ponto final adicionado |
| `ProcessingModule` | `en` | Ponto final adicionado |
| `ProcessingModule` | `pt-br` | Ponto final adicionado |
| `ProjectAcronym` | `pt-br` | Ponto final adicionado |
| `ProjectDrawingCode` | `pt-br` | Ponto final adicionado |
| `PumpingModule` | `en` | Ponto final adicionado |
| `PumpingModule` | `pt-br` | Ponto final adicionado |
| `ReliefValve` | `en` | Ponto final adicionado |
| `ReliefValve` | `pt-br` | Ponto final adicionado |
| `RigidJumper` | `en` | Ponto final adicionado |
| `RigidJumper` | `pt-br` | Ponto final adicionado |
| `RiserBalcony` | `pt-br` | Ponto final adicionado |
| `RiserSpan` | `en` | Ponto final adicionado |
| `RiserSpan` | `pt-br` | Ponto final adicionado |
| `RiserSupport` | `en` | Ponto final adicionado |
| `RiserSupport` | `pt-br` | Ponto final adicionado |
| `RoboticActuator` | `en` | Ponto final adicionado |
| `RoboticActuator` | `pt-br` | Ponto final adicionado |
| `ROVTool` | `en` | Ponto final adicionado |
| `RunningTool` | `en` | Ponto final adicionado |
| `RunningTool` | `pt-br` | Ponto final adicionado |
| `SCM` | `en` | Ponto final adicionado |
| `SCM` | `pt-br` | Ponto final adicionado |
| `SCMMB` | `en` | Ponto final adicionado |
| `SCMMB` | `pt-br` | Ponto final adicionado |
| `Service` | `pt-br` | Ponto final adicionado |
| `Shackle` | `pt-br` | Ponto final adicionado |
| `Socket` | `en` | Ponto final adicionado |
| `Socket` | `pt-br` | Ponto final adicionado |
| `SolidLayer` | `pt-br` | Ponto final adicionado |
| `SolubilityTable_MoleculeIdentifier` | `pt-br` | Ponto final adicionado |
| `SpecialRequirements` | `pt-br` | Ponto final adicionado |
| `SpecificHeatCapacity` | `pt-br` | Ponto final adicionado |
| `SpecificWeight` | `pt-br` | Ponto final adicionado |
| `StaticUmbilicalSpan` | `en` | Ponto final adicionado |
| `StaticUmbilicalSpan` | `pt-br` | Ponto final adicionado |
| `StiffTorsionalStiffnessAtSeaLevel` | `pt-br` | Ponto final adicionado |
| `StorageSkid` | `en` | Ponto final adicionado |
| `StorageSkid` | `pt-br` | Ponto final adicionado |
| `StorageSpool` | `en` | Ponto final adicionado |
| `StorageSpool` | `pt-br` | Ponto final adicionado |
| `StrIntOffPLevMaxPress` | `pt-br` | Ponto final adicionado |
| `StrIntOffPLevMaxPressValRef` | `pt-br` | Ponto final adicionado |
| `StrIntOffPLevNomPress` | `pt-br` | Ponto final adicionado |
| `StrIntOffPLevNomPressValRef` | `pt-br` | Ponto final adicionado |
| `StrIntOnNoTensMaxPress` | `pt-br` | Ponto final adicionado |
| `StrIntOnNoTensMaxPressValRef` | `pt-br` | Ponto final adicionado |
| `StrIntOnNoTensNomPress` | `pt-br` | Ponto final adicionado |
| `StrIntOnNoTensNomPressValRef` | `pt-br` | Ponto final adicionado |
| `Structure` | `en` | Ponto final adicionado |
| `Structure` | `pt-br` | Ponto final adicionado |
| `StructureApplicationsList` | `pt-br` | Ponto final adicionado |
| `SubseaEquipment` | `en` | Ponto final adicionado |
| `SubseaEquipment` | `pt-br` | Ponto final adicionado |
| `SuctionPile` | `en` | Ponto final adicionado |
| `SuctionPile` | `pt-br` | Ponto final adicionado |
| `TapesQuantity` | `en` | Ponto final adicionado |
| `TensileArmourAnnulusCondition` | `pt-br` | Ponto final adicionado |
| `TensionerPadsMaterial` | `pt-br` | Ponto final adicionado |
| `TensionerPadsShape` | `pt-br` | Ponto final adicionado |
| `TensionerTracksQuantity` | `pt-br` | Ponto final adicionado |
| `TestConditions` | `pt-br` | Ponto final adicionado |
| `ThermalConductivityCoefficient` | `pt-br` | Ponto final adicionado |
| `ThreadsPerInch` | `en` | Ponto final adicionado |
| `TorpedoPile` | `en` | Ponto final adicionado |
| `TorpedoPile` | `pt-br` | Ponto final adicionado |
| `TransportLineSegment` | `pt-br` | Ponto final adicionado |
| `TubingHanger` | `en` | Ponto final adicionado |
| `TubingHanger` | `pt-br` | Ponto final adicionado |
| `TypeLevelAttribute` | `en` | Ponto final adicionado |
| `TypeLevelAttribute` | `pt-br` | Ponto final adicionado |
| `UltimateTensileStress` | `pt-br` | Ponto final adicionado |
| `UTA` | `en` | Ponto final adicionado |
| `UTA` | `pt-br` | Ponto final adicionado |
| `validValues` | `en` | Ponto final adicionado |
| `validValues` | `pt-br` | Ponto final adicionado |
| `ValueOrigin` | `en` | Ponto final adicionado |
| `ValueOrigin` | `pt-br` | Ponto final adicionado |
| `WearBushing` | `en` | Ponto final adicionado |
| `WearBushing` | `pt-br` | Ponto final adicionado |
| `WetChristmasTree` | `en` | Ponto final adicionado |
| `WetChristmasTree` | `pt-br` | Ponto final adicionado |
| `WireRopeQuantity` | `en` | Ponto final adicionado |
| `WireRopeSlingDiameter` | `pt-br` | Ponto final adicionado |
| `WoundLayer` | `pt-br` | Ponto final adicionado |

## 🔍 Issues de Qualidade (Requerem Decisão do Especialista)

*Estes issues NÃO são corrigidos automaticamente. Requerem análise do especialista em ontologias.*

### 🏷️ Issues de DomainAttribute

> **Formato de cada item:**
> - **`Nome da Entidade`** — `CÓDIGO_DO_ERRO`
>   - Descrição detalhada do problema encontrado

#### ⚠️ Avisos para Revisão (510)

- **`AbsoluteInsidePressure`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'AbsoluteInsidePressure' não possui skos:definition em português (@pt-br)
- **`AbsoluteOutsidePressure`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'AbsoluteOutsidePressure' não possui skos:definition em português (@pt-br)
- **`AnodeCollarsAxialSpacing`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'AnodeCollarsAxialSpacing' não possui skos:definition em português (@pt-br)
- **`AnodeCollarsQuantity`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'AnodeCollarsQuantity' não possui skos:definition em português (@pt-br)
- **`AssemblyShouldObeyModelPolarity`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'AssemblyShouldObeyModelPolarity' não possui skos:definition em português (@pt-br)
- **`AssemblyTorque`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'AssemblyTorque' não possui skos:definition em português (@pt-br)
- **`BendingMomentTable_BendingMoment`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'BendingMomentTable_BendingMoment' não possui skos:definition em português (@pt-br)
- **`BendingMomentTable_Curvature`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'BendingMomentTable_Curvature' não possui skos:definition em português (@pt-br)
- **`BendingStiffnessCurveAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'BendingStiffnessCurveAttribute' não possui dcterms:accessRights
- **`BendingStiffnessCurveAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'BendingStiffnessCurveAttribute' não possui skos:definition em inglês (@en)
- **`BendingStiffnessCurveAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'BendingStiffnessCurveAttribute' não possui skos:definition em português (@pt-br)
- **`BendingStiffnessCurveAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'BendingStiffnessCurveAttribute' não possui dcterms:identifier
- **`BendingStiffnessCurveAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'BendingStiffnessCurveAttribute' não possui skos:prefLabel em inglês (@en)
- **`BendingStiffnessCurveAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'BendingStiffnessCurveAttribute' não possui skos:prefLabel em português (@pt-br)
- **`BendingStiffnessCurveAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'BendingStiffnessCurveAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'BendingStiffnessCurveAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'BendingStiffnessCurveAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'BendingStiffnessCurveAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`BendingStiffnessTableColumn`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'BendingStiffnessTableColumn' não possui dcterms:accessRights
- **`BendingStiffnessTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'BendingStiffnessTableColumn' não possui skos:definition em inglês (@en)
- **`BendingStiffnessTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'BendingStiffnessTableColumn' não possui skos:definition em português (@pt-br)
- **`BendingStiffnessTableColumn`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'BendingStiffnessTableColumn' não possui dcterms:identifier
- **`BendingStiffnessTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'BendingStiffnessTableColumn' não possui skos:prefLabel em inglês (@en)
- **`BendingStiffnessTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'BendingStiffnessTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`BendingStiffnessTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'BendingStiffnessTableColumn' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'BendingStiffnessTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'BendingStiffnessTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'BendingStiffnessTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`BendMomentVsShearForceCurveAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui dcterms:accessRights
- **`BendMomentVsShearForceCurveAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui skos:definition em inglês (@en)
- **`BendMomentVsShearForceCurveAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui skos:definition em português (@pt-br)
- **`BendMomentVsShearForceCurveAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui dcterms:identifier
- **`BendMomentVsShearForceCurveAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui skos:prefLabel em inglês (@en)
- **`BendMomentVsShearForceCurveAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui skos:prefLabel em português (@pt-br)
- **`BendMomentVsShearForceCurveAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`BendMomentVsShearForceTable_BendingMoment`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'BendMomentVsShearForceTable_BendingMoment' não possui skos:definition em português (@pt-br)
- **`BendMomentVsShearForceTable_Condition`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'BendMomentVsShearForceTable_Condition' não possui skos:definition em português (@pt-br)
- **`BendMomentVsShearForceTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'BendMomentVsShearForceTableColumn' não possui skos:definition em português (@pt-br)
- **`BendMomentVsShearForceTableColumn`** — `DOMAINATTR_IDENTIFIER_MISMATCH`
  - dcterms:identifier 'BendMomentVsShearForceTable' não corresponde ao local name 'BendMomentVsShearForceTableColumn'
- **`BendMomentVsShearForceTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'BendMomentVsShearForceTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'BendMomentVsShearForceTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'BendMomentVsShearForceTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`BoreDiameter`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'BoreDiameter' não possui skos:definition em português (@pt-br)
- **`CalculatedAbsoluteBurstPressure`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'CalculatedAbsoluteBurstPressure' não possui skos:definition em português (@pt-br)
- **`ClampInternalDiameter`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ClampInternalDiameter' não possui skos:definition em português (@pt-br)
- **`CO2VolumePercentage`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'CO2VolumePercentage' não possui skos:definition em português (@pt-br)
- **`CollarInternalDiameter`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'CollarInternalDiameter' não possui skos:definition em português (@pt-br)
- **`CompositeLayerMaterialType`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'CompositeLayerMaterialType' não possui skos:definition em português (@pt-br)
- **`CriticalCurvatureOfSlipping`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'CriticalCurvatureOfSlipping' não possui skos:definition em português (@pt-br)
- **`CrushingCurveAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'CrushingCurveAttribute' não possui dcterms:accessRights
- **`CrushingCurveAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'CrushingCurveAttribute' não possui skos:definition em inglês (@en)
- **`CrushingCurveAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'CrushingCurveAttribute' não possui skos:definition em português (@pt-br)
- **`CrushingCurveAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'CrushingCurveAttribute' não possui dcterms:identifier
- **`CrushingCurveAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'CrushingCurveAttribute' não possui skos:prefLabel em inglês (@en)
- **`CrushingCurveAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'CrushingCurveAttribute' não possui skos:prefLabel em português (@pt-br)
- **`CrushingCurveAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'CrushingCurveAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'CrushingCurveAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'CrushingCurveAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'CrushingCurveAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`CrushingFrictionCoefficientTighteningAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui dcterms:accessRights
- **`CrushingFrictionCoefficientTighteningAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui skos:definition em inglês (@en)
- **`CrushingFrictionCoefficientTighteningAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui skos:definition em português (@pt-br)
- **`CrushingFrictionCoefficientTighteningAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui dcterms:identifier
- **`CrushingFrictionCoefficientTighteningAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui skos:prefLabel em inglês (@en)
- **`CrushingFrictionCoefficientTighteningAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui skos:prefLabel em português (@pt-br)
- **`CrushingFrictionCoefficientTighteningAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`CrushingFrictionCoefficientTighteningTableColumn`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'CrushingFrictionCoefficientTighteningTableColumn' não possui dcterms:accessRights
- **`CrushingFrictionCoefficientTighteningTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'CrushingFrictionCoefficientTighteningTableColumn' não possui skos:definition em inglês (@en)
- **`CrushingFrictionCoefficientTighteningTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'CrushingFrictionCoefficientTighteningTableColumn' não possui skos:definition em português (@pt-br)
- **`CrushingFrictionCoefficientTighteningTableColumn`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'CrushingFrictionCoefficientTighteningTableColumn' não possui dcterms:identifier
- **`CrushingFrictionCoefficientTighteningTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'CrushingFrictionCoefficientTighteningTableColumn' não possui skos:prefLabel em inglês (@en)
- **`CrushingFrictionCoefficientTighteningTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'CrushingFrictionCoefficientTighteningTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`CrushingFrictionCoefficientTighteningTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'CrushingFrictionCoefficientTighteningTableColumn' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'CrushingFrictionCoefficientTighteningTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'CrushingFrictionCoefficientTighteningTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'CrushingFrictionCoefficientTighteningTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`CrushingMaximumAllowableTensionAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'CrushingMaximumAllowableTensionAttribute' não possui dcterms:accessRights
- **`CrushingMaximumAllowableTensionAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'CrushingMaximumAllowableTensionAttribute' não possui skos:definition em inglês (@en)
- **`CrushingMaximumAllowableTensionAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'CrushingMaximumAllowableTensionAttribute' não possui skos:definition em português (@pt-br)
- **`CrushingMaximumAllowableTensionAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'CrushingMaximumAllowableTensionAttribute' não possui dcterms:identifier
- **`CrushingMaximumAllowableTensionAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'CrushingMaximumAllowableTensionAttribute' não possui skos:prefLabel em inglês (@en)
- **`CrushingMaximumAllowableTensionAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'CrushingMaximumAllowableTensionAttribute' não possui skos:prefLabel em português (@pt-br)
- **`CrushingMaximumAllowableTensionAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'CrushingMaximumAllowableTensionAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'CrushingMaximumAllowableTensionAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'CrushingMaximumAllowableTensionAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'CrushingMaximumAllowableTensionAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`CrushingMaximumAllowableTensionTableColumn`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'CrushingMaximumAllowableTensionTableColumn' não possui dcterms:accessRights
- **`CrushingMaximumAllowableTensionTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'CrushingMaximumAllowableTensionTableColumn' não possui skos:definition em inglês (@en)
- **`CrushingMaximumAllowableTensionTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'CrushingMaximumAllowableTensionTableColumn' não possui skos:definition em português (@pt-br)
- **`CrushingMaximumAllowableTensionTableColumn`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'CrushingMaximumAllowableTensionTableColumn' não possui dcterms:identifier
- **`CrushingMaximumAllowableTensionTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'CrushingMaximumAllowableTensionTableColumn' não possui skos:prefLabel em inglês (@en)
- **`CrushingMaximumAllowableTensionTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'CrushingMaximumAllowableTensionTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`CrushingMaximumAllowableTensionTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'CrushingMaximumAllowableTensionTableColumn' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'CrushingMaximumAllowableTensionTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'CrushingMaximumAllowableTensionTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'CrushingMaximumAllowableTensionTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`CrushingMaximumAllowableTighteningAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'CrushingMaximumAllowableTighteningAttribute' não possui dcterms:accessRights
- **`CrushingMaximumAllowableTighteningAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'CrushingMaximumAllowableTighteningAttribute' não possui skos:definition em inglês (@en)
- **`CrushingMaximumAllowableTighteningAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'CrushingMaximumAllowableTighteningAttribute' não possui skos:definition em português (@pt-br)
- **`CrushingMaximumAllowableTighteningAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'CrushingMaximumAllowableTighteningAttribute' não possui dcterms:identifier
- **`CrushingMaximumAllowableTighteningAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'CrushingMaximumAllowableTighteningAttribute' não possui skos:prefLabel em inglês (@en)
- **`CrushingMaximumAllowableTighteningAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'CrushingMaximumAllowableTighteningAttribute' não possui skos:prefLabel em português (@pt-br)
- **`CrushingMaximumAllowableTighteningAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'CrushingMaximumAllowableTighteningAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'CrushingMaximumAllowableTighteningAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'CrushingMaximumAllowableTighteningAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'CrushingMaximumAllowableTighteningAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`CrushingMaximumAllowableTighteningTableColumn`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'CrushingMaximumAllowableTighteningTableColumn' não possui dcterms:accessRights
- **`CrushingMaximumAllowableTighteningTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'CrushingMaximumAllowableTighteningTableColumn' não possui skos:definition em inglês (@en)
- **`CrushingMaximumAllowableTighteningTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'CrushingMaximumAllowableTighteningTableColumn' não possui skos:definition em português (@pt-br)
- **`CrushingMaximumAllowableTighteningTableColumn`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'CrushingMaximumAllowableTighteningTableColumn' não possui dcterms:identifier
- **`CrushingMaximumAllowableTighteningTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'CrushingMaximumAllowableTighteningTableColumn' não possui skos:prefLabel em inglês (@en)
- **`CrushingMaximumAllowableTighteningTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'CrushingMaximumAllowableTighteningTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`CrushingMaximumAllowableTighteningTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'CrushingMaximumAllowableTighteningTableColumn' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'CrushingMaximumAllowableTighteningTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'CrushingMaximumAllowableTighteningTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'CrushingMaximumAllowableTighteningTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`DamagingPullInStraightLine`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'DamagingPullInStraightLine' não possui skos:definition em português (@pt-br)
- **`DiffusionCurveAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'DiffusionCurveAttribute' não possui dcterms:accessRights
- **`DiffusionCurveAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'DiffusionCurveAttribute' não possui skos:definition em inglês (@en)
- **`DiffusionCurveAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'DiffusionCurveAttribute' não possui skos:definition em português (@pt-br)
- **`DiffusionCurveAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'DiffusionCurveAttribute' não possui dcterms:identifier
- **`DiffusionCurveAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'DiffusionCurveAttribute' não possui skos:prefLabel em inglês (@en)
- **`DiffusionCurveAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'DiffusionCurveAttribute' não possui skos:prefLabel em português (@pt-br)
- **`DiffusionCurveAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'DiffusionCurveAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'DiffusionCurveAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'DiffusionCurveAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'DiffusionCurveAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`DiffusionTable_DiffusionCoefficient`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'DiffusionTable_DiffusionCoefficient' não possui skos:definition em português (@pt-br)
- **`DiffusionTable_Temperature`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'DiffusionTable_Temperature' não possui skos:definition em português (@pt-br)
- **`DiffusionTableColumn`** — `DOMAINATTR_IDENTIFIER_MISMATCH`
  - dcterms:identifier 'DiffusionTable' não corresponde ao local name 'DiffusionTableColumn'
- **`DiffusionTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'DiffusionTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'DiffusionTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'DiffusionTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`DimensionsTableColumn`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'DimensionsTableColumn' não possui dcterms:accessRights
- **`DimensionsTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'DimensionsTableColumn' não possui skos:definition em inglês (@en)
- **`DimensionsTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'DimensionsTableColumn' não possui skos:definition em português (@pt-br)
- **`DimensionsTableColumn`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'DimensionsTableColumn' não possui dcterms:identifier
- **`DimensionsTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'DimensionsTableColumn' não possui skos:prefLabel em inglês (@en)
- **`DimensionsTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'DimensionsTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`DimensionsTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'DimensionsTableColumn' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'DimensionsTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'DimensionsTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'DimensionsTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`DisplacedVolume`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'DisplacedVolume' não possui skos:definition em português (@pt-br)
- **`DrawingDimensionsTable_DimensionName`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'DrawingDimensionsTable_DimensionName' não possui skos:definition em português (@pt-br)
- **`DrawingDimensionsTable_DimensionValue`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'DrawingDimensionsTable_DimensionValue' não possui skos:definition em português (@pt-br)
- **`DrawingDimensionsTableAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'DrawingDimensionsTableAttribute' não possui dcterms:accessRights
- **`DrawingDimensionsTableAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'DrawingDimensionsTableAttribute' não possui skos:definition em inglês (@en)
- **`DrawingDimensionsTableAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'DrawingDimensionsTableAttribute' não possui skos:definition em português (@pt-br)
- **`DrawingDimensionsTableAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'DrawingDimensionsTableAttribute' não possui dcterms:identifier
- **`DrawingDimensionsTableAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'DrawingDimensionsTableAttribute' não possui skos:prefLabel em inglês (@en)
- **`DrawingDimensionsTableAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'DrawingDimensionsTableAttribute' não possui skos:prefLabel em português (@pt-br)
- **`DrawingDimensionsTableAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'DrawingDimensionsTableAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'DrawingDimensionsTableAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'DrawingDimensionsTableAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'DrawingDimensionsTableAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`EarlyLeakMaxPressTable_TensLimitValRef`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'EarlyLeakMaxPressTable_TensLimitValRef' não possui skos:definition em português (@pt-br)
- **`EarlyLeakMaxPressTableAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'EarlyLeakMaxPressTableAttribute' não possui dcterms:accessRights
- **`EarlyLeakMaxPressTableAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'EarlyLeakMaxPressTableAttribute' não possui skos:definition em inglês (@en)
- **`EarlyLeakMaxPressTableAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'EarlyLeakMaxPressTableAttribute' não possui skos:definition em português (@pt-br)
- **`EarlyLeakMaxPressTableAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'EarlyLeakMaxPressTableAttribute' não possui dcterms:identifier
- **`EarlyLeakMaxPressTableAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'EarlyLeakMaxPressTableAttribute' não possui skos:prefLabel em inglês (@en)
- **`EarlyLeakMaxPressTableAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'EarlyLeakMaxPressTableAttribute' não possui skos:prefLabel em português (@pt-br)
- **`EarlyLeakMaxPressTableAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'EarlyLeakMaxPressTableAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'EarlyLeakMaxPressTableAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'EarlyLeakMaxPressTableAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'EarlyLeakMaxPressTableAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`EarlyLeakMaxPressTableColumn`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'EarlyLeakMaxPressTableColumn' não possui dcterms:accessRights
- **`EarlyLeakMaxPressTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'EarlyLeakMaxPressTableColumn' não possui skos:definition em inglês (@en)
- **`EarlyLeakMaxPressTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'EarlyLeakMaxPressTableColumn' não possui skos:definition em português (@pt-br)
- **`EarlyLeakMaxPressTableColumn`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'EarlyLeakMaxPressTableColumn' não possui dcterms:identifier
- **`EarlyLeakMaxPressTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'EarlyLeakMaxPressTableColumn' não possui skos:prefLabel em inglês (@en)
- **`EarlyLeakMaxPressTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'EarlyLeakMaxPressTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`EarlyLeakMaxPressTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'EarlyLeakMaxPressTableColumn' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'EarlyLeakMaxPressTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'EarlyLeakMaxPressTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'EarlyLeakMaxPressTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`EarlyLeakNomPressTable_PressValRefMult`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'EarlyLeakNomPressTable_PressValRefMult' não possui skos:definition em português (@pt-br)
- **`EarlyLeakNomPressTable_TensLimitValRef`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'EarlyLeakNomPressTable_TensLimitValRef' não possui skos:definition em português (@pt-br)
- **`EarlyLeakNomPressTableAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'EarlyLeakNomPressTableAttribute' não possui dcterms:accessRights
- **`EarlyLeakNomPressTableAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'EarlyLeakNomPressTableAttribute' não possui skos:definition em inglês (@en)
- **`EarlyLeakNomPressTableAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'EarlyLeakNomPressTableAttribute' não possui skos:definition em português (@pt-br)
- **`EarlyLeakNomPressTableAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'EarlyLeakNomPressTableAttribute' não possui dcterms:identifier
- **`EarlyLeakNomPressTableAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'EarlyLeakNomPressTableAttribute' não possui skos:prefLabel em inglês (@en)
- **`EarlyLeakNomPressTableAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'EarlyLeakNomPressTableAttribute' não possui skos:prefLabel em português (@pt-br)
- **`EarlyLeakNomPressTableAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'EarlyLeakNomPressTableAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'EarlyLeakNomPressTableAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'EarlyLeakNomPressTableAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'EarlyLeakNomPressTableAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`EarlyLeakNomPressTableColumn`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'EarlyLeakNomPressTableColumn' não possui dcterms:accessRights
- **`EarlyLeakNomPressTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'EarlyLeakNomPressTableColumn' não possui skos:definition em inglês (@en)
- **`EarlyLeakNomPressTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'EarlyLeakNomPressTableColumn' não possui skos:definition em português (@pt-br)
- **`EarlyLeakNomPressTableColumn`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'EarlyLeakNomPressTableColumn' não possui dcterms:identifier
- **`EarlyLeakNomPressTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'EarlyLeakNomPressTableColumn' não possui skos:prefLabel em inglês (@en)
- **`EarlyLeakNomPressTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'EarlyLeakNomPressTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`EarlyLeakNomPressTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'EarlyLeakNomPressTableColumn' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'EarlyLeakNomPressTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'EarlyLeakNomPressTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'EarlyLeakNomPressTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`EModVsTempCurveAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'EModVsTempCurveAttribute' não possui dcterms:accessRights
- **`EModVsTempCurveAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'EModVsTempCurveAttribute' não possui skos:definition em inglês (@en)
- **`EModVsTempCurveAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'EModVsTempCurveAttribute' não possui skos:definition em português (@pt-br)
- **`EModVsTempCurveAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'EModVsTempCurveAttribute' não possui dcterms:identifier
- **`EModVsTempCurveAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'EModVsTempCurveAttribute' não possui skos:prefLabel em inglês (@en)
- **`EModVsTempCurveAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'EModVsTempCurveAttribute' não possui skos:prefLabel em português (@pt-br)
- **`EModVsTempCurveAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'EModVsTempCurveAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'EModVsTempCurveAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'EModVsTempCurveAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'EModVsTempCurveAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`EModVsTempTable_Temperature`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'EModVsTempTable_Temperature' não possui skos:definition em português (@pt-br)
- **`EModVsTempTable_Temperature`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'EModVsTempTable_Temperature' não possui skos:prefLabel em português (@pt-br)
- **`EModVsTempTableColumn`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'EModVsTempTableColumn' não possui dcterms:accessRights
- **`EModVsTempTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'EModVsTempTableColumn' não possui skos:definition em inglês (@en)
- **`EModVsTempTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'EModVsTempTableColumn' não possui skos:definition em português (@pt-br)
- **`EModVsTempTableColumn`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'EModVsTempTableColumn' não possui dcterms:identifier
- **`EModVsTempTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'EModVsTempTableColumn' não possui skos:prefLabel em inglês (@en)
- **`EModVsTempTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'EModVsTempTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`EModVsTempTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'EModVsTempTableColumn' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'EModVsTempTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'EModVsTempTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'EModVsTempTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`ErosionalVelocity`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ErosionalVelocity' não possui skos:definition em português (@pt-br)
- **`ExternalDiameter`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ExternalDiameter' não possui skos:definition em português (@pt-br)
- **`FatMaxPressValRefMult`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'FatMaxPressValRefMult' não possui skos:definition em português (@pt-br)
- **`FatNomPressValRefMult`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'FatNomPressValRefMult' não possui skos:definition em português (@pt-br)
- **`FlangeAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'FlangeAttribute' não possui dcterms:accessRights
- **`FlangeAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'FlangeAttribute' não possui skos:definition em inglês (@en)
- **`FlangeAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'FlangeAttribute' não possui skos:definition em português (@pt-br)
- **`FlangeAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'FlangeAttribute' não possui dcterms:identifier
- **`FlangeAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'FlangeAttribute' não possui skos:prefLabel em inglês (@en)
- **`FlangeAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'FlangeAttribute' não possui skos:prefLabel em português (@pt-br)
- **`FlangeAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'FlangeAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'FlangeAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'FlangeAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'FlangeAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`FlangeFaceType`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'FlangeFaceType' não possui skos:definition em português (@pt-br)
- **`FlangeType`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'FlangeType' não possui skos:definition em português (@pt-br)
- **`FlexibleStructureServicesList`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'FlexibleStructureServicesList' não possui skos:definition em português (@pt-br)
- **`FrictionCoefficientTighteningTable_CoefficientOfFriction`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'FrictionCoefficientTighteningTable_CoefficientOfFriction' não possui skos:definition em português (@pt-br)
- **`FrictionCoefficientTighteningTable_TighteningPerTrack`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'FrictionCoefficientTighteningTable_TighteningPerTrack' não possui skos:definition em português (@pt-br)
- **`FullyThreaded`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'FullyThreaded' não possui skos:definition em português (@pt-br)
- **`GalvanicMaterial`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'GalvanicMaterial' não possui skos:definition em português (@pt-br)
- **`GrooveDiameter`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'GrooveDiameter' não possui skos:definition em português (@pt-br)
- **`GrooveHeight`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'GrooveHeight' não possui skos:definition em português (@pt-br)
- **`GrooveMinimumSupportArea`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'GrooveMinimumSupportArea' não possui skos:definition em português (@pt-br)
- **`GrooveSupportSurfaceDiameter`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'GrooveSupportSurfaceDiameter' não possui skos:definition em português (@pt-br)
- **`H2SVolumeConcentration`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'H2SVolumeConcentration' não possui skos:definition em português (@pt-br)
- **`HasFaceORing`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'HasFaceORing' não possui skos:definition em português (@pt-br)
- **`HasModaSensor`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'HasModaSensor' não possui skos:definition em português (@pt-br)
- **`HasN2InjectionPort`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'HasN2InjectionPort' não possui skos:definition em português (@pt-br)
- **`HasThermalInsulation`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'HasThermalInsulation' não possui skos:definition em inglês (@en)
- **`HasThermalInsulation`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'HasThermalInsulation' não possui skos:definition em português (@pt-br)
- **`HydrostaticPressureTestsAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'HydrostaticPressureTestsAttribute' não possui dcterms:accessRights
- **`HydrostaticPressureTestsAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'HydrostaticPressureTestsAttribute' não possui skos:definition em inglês (@en)
- **`HydrostaticPressureTestsAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'HydrostaticPressureTestsAttribute' não possui skos:definition em português (@pt-br)
- **`HydrostaticPressureTestsAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'HydrostaticPressureTestsAttribute' não possui dcterms:identifier
- **`HydrostaticPressureTestsAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'HydrostaticPressureTestsAttribute' não possui skos:prefLabel em inglês (@en)
- **`HydrostaticPressureTestsAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'HydrostaticPressureTestsAttribute' não possui skos:prefLabel em português (@pt-br)
- **`HydrostaticPressureTestsAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'HydrostaticPressureTestsAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'HydrostaticPressureTestsAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'HydrostaticPressureTestsAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'HydrostaticPressureTestsAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`IndividualAnodeMass`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'IndividualAnodeMass' não possui skos:definition em português (@pt-br)
- **`InsideTemperature`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'InsideTemperature' não possui skos:definition em português (@pt-br)
- **`IntermediateValuesStrategy`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'IntermediateValuesStrategy' não possui skos:definition em português (@pt-br)
- **`InternalDiameter`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'InternalDiameter' não possui skos:definition em português (@pt-br)
- **`InternalIncidentalPressureCurveAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'InternalIncidentalPressureCurveAttribute' não possui skos:definition em português (@pt-br)
- **`InternalIncidentalPressureCurveAttribute`** — `DOMAINATTR_IDENTIFIER_MISMATCH`
  - dcterms:identifier 'InternalIncidentalPressureTable' não corresponde ao local name 'InternalIncidentalPressureCurveAttribute'
- **`InternalIncidentalPressureCurveAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'InternalIncidentalPressureCurveAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'InternalIncidentalPressureCurveAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`InternalIncidentalPressureTable_Pressure`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'InternalIncidentalPressureTable_Pressure' não possui skos:definition em português (@pt-br)
- **`InternalIncidentalPressureTableColumn`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'InternalIncidentalPressureTableColumn' não possui dcterms:accessRights
- **`InternalIncidentalPressureTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'InternalIncidentalPressureTableColumn' não possui skos:definition em inglês (@en)
- **`InternalIncidentalPressureTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'InternalIncidentalPressureTableColumn' não possui skos:definition em português (@pt-br)
- **`InternalIncidentalPressureTableColumn`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'InternalIncidentalPressureTableColumn' não possui dcterms:identifier
- **`InternalIncidentalPressureTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'InternalIncidentalPressureTableColumn' não possui skos:prefLabel em inglês (@en)
- **`InternalIncidentalPressureTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'InternalIncidentalPressureTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`InternalIncidentalPressureTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'InternalIncidentalPressureTableColumn' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'InternalIncidentalPressureTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'InternalIncidentalPressureTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`InternalVolume`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'InternalVolume' não possui skos:definition em português (@pt-br)
- **`IsSpare`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'IsSpare' não possui skos:definition em português (@pt-br)
- **`LayerGeometryAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'LayerGeometryAttribute' não possui dcterms:accessRights
- **`LayerGeometryAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'LayerGeometryAttribute' não possui skos:definition em inglês (@en)
- **`LayerGeometryAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayerGeometryAttribute' não possui skos:definition em português (@pt-br)
- **`LayerGeometryAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'LayerGeometryAttribute' não possui dcterms:identifier
- **`LayerGeometryAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'LayerGeometryAttribute' não possui skos:prefLabel em inglês (@en)
- **`LayerGeometryAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'LayerGeometryAttribute' não possui skos:prefLabel em português (@pt-br)
- **`LayerGeometryAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'LayerGeometryAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'LayerGeometryAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'LayerGeometryAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'LayerGeometryAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`LayerGeometryCrossSection`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayerGeometryCrossSection' não possui skos:definition em português (@pt-br)
- **`LayerGeometryInertiaX`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayerGeometryInertiaX' não possui skos:definition em português (@pt-br)
- **`LayerGeometryInertiaY`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayerGeometryInertiaY' não possui skos:definition em português (@pt-br)
- **`LayerGeometryManufacturer`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayerGeometryManufacturer' não possui skos:definition em português (@pt-br)
- **`LayerGeometryName`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayerGeometryName' não possui skos:definition em português (@pt-br)
- **`LayerGeometryProfileThickness`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayerGeometryProfileThickness' não possui skos:definition em português (@pt-br)
- **`LayerGeometryProfileWidth`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayerGeometryProfileWidth' não possui skos:definition em português (@pt-br)
- **`LayerGeometryThickness`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayerGeometryThickness' não possui skos:definition em português (@pt-br)
- **`LayerThickness`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayerThickness' não possui skos:definition em português (@pt-br)
- **`LayerWatertight`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayerWatertight' não possui skos:definition em português (@pt-br)
- **`LayingMinimumRadiusCurveAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'LayingMinimumRadiusCurveAttribute' não possui dcterms:accessRights
- **`LayingMinimumRadiusCurveAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'LayingMinimumRadiusCurveAttribute' não possui skos:definition em inglês (@en)
- **`LayingMinimumRadiusCurveAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayingMinimumRadiusCurveAttribute' não possui skos:definition em português (@pt-br)
- **`LayingMinimumRadiusCurveAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'LayingMinimumRadiusCurveAttribute' não possui dcterms:identifier
- **`LayingMinimumRadiusCurveAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'LayingMinimumRadiusCurveAttribute' não possui skos:prefLabel em inglês (@en)
- **`LayingMinimumRadiusCurveAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'LayingMinimumRadiusCurveAttribute' não possui skos:prefLabel em português (@pt-br)
- **`LayingMinimumRadiusCurveAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'LayingMinimumRadiusCurveAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'LayingMinimumRadiusCurveAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'LayingMinimumRadiusCurveAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'LayingMinimumRadiusCurveAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`LayingMinimumRadiusTable_AbsoluteExternalPressure`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayingMinimumRadiusTable_AbsoluteExternalPressure' não possui skos:definition em português (@pt-br)
- **`LayingMinimumRadiusTable_AbsoluteInternalPressure`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayingMinimumRadiusTable_AbsoluteInternalPressure' não possui skos:definition em português (@pt-br)
- **`LayingMinimumRadiusTable_MinimumAllowableBendingRadius`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayingMinimumRadiusTable_MinimumAllowableBendingRadius' não possui skos:definition em português (@pt-br)
- **`LayingMinimumRadiusTable_SectionSupportedByRigidSupport`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayingMinimumRadiusTable_SectionSupportedByRigidSupport' não possui skos:definition em português (@pt-br)
- **`LayingMinimumRadiusTableColumn`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'LayingMinimumRadiusTableColumn' não possui dcterms:accessRights
- **`LayingMinimumRadiusTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'LayingMinimumRadiusTableColumn' não possui skos:definition em inglês (@en)
- **`LayingMinimumRadiusTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LayingMinimumRadiusTableColumn' não possui skos:definition em português (@pt-br)
- **`LayingMinimumRadiusTableColumn`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'LayingMinimumRadiusTableColumn' não possui dcterms:identifier
- **`LayingMinimumRadiusTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'LayingMinimumRadiusTableColumn' não possui skos:prefLabel em inglês (@en)
- **`LayingMinimumRadiusTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'LayingMinimumRadiusTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`LayingMinimumRadiusTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'LayingMinimumRadiusTableColumn' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'LayingMinimumRadiusTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'LayingMinimumRadiusTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'LayingMinimumRadiusTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`LinearMass`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LinearMass' não possui skos:definition em português (@pt-br)
- **`Lubricant`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'Lubricant' não possui skos:definition em português (@pt-br)
- **`LubricantFrictionFactor`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'LubricantFrictionFactor' não possui skos:definition em português (@pt-br)
- **`ManufacturerDefinedMaterialName`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ManufacturerDefinedMaterialName' não possui skos:definition em português (@pt-br)
- **`ManufacturingDate`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ManufacturingDate' não possui skos:definition em português (@pt-br)
- **`ManufacturingNonConformities`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ManufacturingNonConformities' não possui skos:definition em português (@pt-br)
- **`Mass`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'Mass' não possui skos:definition em português (@pt-br)
- **`MaterialManufacturerAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'MaterialManufacturerAttribute' não possui dcterms:accessRights
- **`MaterialManufacturerAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'MaterialManufacturerAttribute' não possui skos:definition em inglês (@en)
- **`MaterialManufacturerAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaterialManufacturerAttribute' não possui skos:definition em português (@pt-br)
- **`MaterialManufacturerAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'MaterialManufacturerAttribute' não possui dcterms:identifier
- **`MaterialManufacturerAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'MaterialManufacturerAttribute' não possui skos:prefLabel em inglês (@en)
- **`MaterialManufacturerAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'MaterialManufacturerAttribute' não possui skos:prefLabel em português (@pt-br)
- **`MaterialManufacturerAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'MaterialManufacturerAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'MaterialManufacturerAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'MaterialManufacturerAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'MaterialManufacturerAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`MaterialRequest`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaterialRequest' não possui skos:definition em português (@pt-br)
- **`MaterialRequestRev`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaterialRequestRev' não possui skos:definition em português (@pt-br)
- **`MaterialSupplierName`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaterialSupplierName' não possui skos:definition em português (@pt-br)
- **`MaxDesignAbsIntPresCurveAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaxDesignAbsIntPresCurveAttribute' não possui skos:definition em português (@pt-br)
- **`MaxDesignAbsIntPresCurveAttribute`** — `DOMAINATTR_IDENTIFIER_MISMATCH`
  - dcterms:identifier 'MaxDesignAbsIntPresTable' não corresponde ao local name 'MaxDesignAbsIntPresCurveAttribute'
- **`MaxDesignAbsIntPresCurveAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'MaxDesignAbsIntPresCurveAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'MaxDesignAbsIntPresCurveAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`MaxDesignAbsIntPresTable_Pressure`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaxDesignAbsIntPresTable_Pressure' não possui skos:definition em português (@pt-br)
- **`MaxDesignAbsIntPresTableColumn`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'MaxDesignAbsIntPresTableColumn' não possui dcterms:accessRights
- **`MaxDesignAbsIntPresTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'MaxDesignAbsIntPresTableColumn' não possui skos:definition em inglês (@en)
- **`MaxDesignAbsIntPresTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaxDesignAbsIntPresTableColumn' não possui skos:definition em português (@pt-br)
- **`MaxDesignAbsIntPresTableColumn`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'MaxDesignAbsIntPresTableColumn' não possui dcterms:identifier
- **`MaxDesignAbsIntPresTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'MaxDesignAbsIntPresTableColumn' não possui skos:prefLabel em inglês (@en)
- **`MaxDesignAbsIntPresTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'MaxDesignAbsIntPresTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`MaxDesignAbsIntPresTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'MaxDesignAbsIntPresTableColumn' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'MaxDesignAbsIntPresTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'MaxDesignAbsIntPresTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`MaxDesignPressure`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaxDesignPressure' não possui skos:definition em português (@pt-br)
- **`MaxDynamicLoad`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaxDynamicLoad' não possui skos:definition em português (@pt-br)
- **`MaximumAllowableTensileForStraightLine`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaximumAllowableTensileForStraightLine' não possui skos:definition em português (@pt-br)
- **`MaximumAllowableTensionTable_MaximumAllowableTensile`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaximumAllowableTensionTable_MaximumAllowableTensile' não possui skos:definition em português (@pt-br)
- **`MaximumAllowableTensionTable_PulleyRadius`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaximumAllowableTensionTable_PulleyRadius' não possui skos:definition em português (@pt-br)
- **`MaximumAllowableTensionTable_PulleyVAngle`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaximumAllowableTensionTable_PulleyVAngle' não possui skos:definition em português (@pt-br)
- **`MaximumAllowableTighteningTable_AxialLoad`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaximumAllowableTighteningTable_AxialLoad' não possui skos:definition em português (@pt-br)
- **`MaximumAllowableTighteningTable_TighteningPerTrack`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaximumAllowableTighteningTable_TighteningPerTrack' não possui skos:definition em português (@pt-br)
- **`MaximumAmbientTemperature`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaximumAmbientTemperature' não possui skos:definition em português (@pt-br)
- **`MaximumTemperature`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaximumTemperature' não possui skos:definition em português (@pt-br)
- **`MaximumThermalExchangeCoefficient`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaximumThermalExchangeCoefficient' não possui skos:definition em português (@pt-br)
- **`MaxLengthTolerance`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MaxLengthTolerance' não possui skos:definition em português (@pt-br)
- **`MetallicLayerMaterialType`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MetallicLayerMaterialType' não possui skos:definition em português (@pt-br)
- **`MetallicLayerPitch`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MetallicLayerPitch' não possui skos:definition em português (@pt-br)
- **`MetallicStrandLength`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MetallicStrandLength' não possui skos:definition em português (@pt-br)
- **`MetallicStrandSpareQuantity`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MetallicStrandSpareQuantity' não possui skos:definition em português (@pt-br)
- **`MinimumBendingRadiusForStorage`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MinimumBendingRadiusForStorage' não possui skos:definition em português (@pt-br)
- **`MinimumTemperature`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MinimumTemperature' não possui skos:definition em português (@pt-br)
- **`MinimumThermalExchangeCoefficient`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'MinimumThermalExchangeCoefficient' não possui skos:definition em português (@pt-br)
- **`ModulusOfElasticity`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ModulusOfElasticity' não possui skos:definition em português (@pt-br)
- **`NominalDiameter`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'NominalDiameter' não possui skos:definition em português (@pt-br)
- **`NominalLength`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'NominalLength' não possui skos:definition em português (@pt-br)
- **`OffLeakPLevMaxPressValRefMult`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'OffLeakPLevMaxPressValRefMult' não possui skos:definition em português (@pt-br)
- **`OffLeakPLevNomPressValRefMult`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'OffLeakPLevNomPressValRefMult' não possui skos:definition em português (@pt-br)
- **`OuterDiameter`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'OuterDiameter' não possui skos:definition em português (@pt-br)
- **`OutsideTemperature`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'OutsideTemperature' não possui skos:definition em português (@pt-br)
- **`PartNumber`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'PartNumber' não possui skos:definition em português (@pt-br)
- **`PermeabilityCurveAttribute`** — `DOMAINATTR_IDENTIFIER_MISMATCH`
  - dcterms:identifier 'PermeabilityTable' não corresponde ao local name 'PermeabilityCurveAttribute'
- **`PermeabilityCurveAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'PermeabilityCurveAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'PermeabilityCurveAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'PermeabilityCurveAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`PermeabilityTable_PermeabilityCoefficient`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'PermeabilityTable_PermeabilityCoefficient' não possui skos:definition em português (@pt-br)
- **`PermeabilityTable_Temperature`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'PermeabilityTable_Temperature' não possui skos:definition em português (@pt-br)
- **`PermeabilityTableColumn`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'PermeabilityTableColumn' não possui dcterms:accessRights
- **`PermeabilityTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'PermeabilityTableColumn' não possui skos:definition em inglês (@en)
- **`PermeabilityTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'PermeabilityTableColumn' não possui skos:definition em português (@pt-br)
- **`PermeabilityTableColumn`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'PermeabilityTableColumn' não possui dcterms:identifier
- **`PermeabilityTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'PermeabilityTableColumn' não possui skos:prefLabel em inglês (@en)
- **`PermeabilityTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'PermeabilityTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`PermeabilityTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'PermeabilityTableColumn' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'PermeabilityTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'PermeabilityTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'PermeabilityTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`PitchToleranceClass`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'PitchToleranceClass' não possui skos:definition em português (@pt-br)
- **`Planned_Start_Timestamp`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'Planned_Start_Timestamp' não possui skos:definition em inglês (@en)
- **`Planned_Start_Timestamp`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'Planned_Start_Timestamp' não possui skos:definition em português (@pt-br)
- **`Planned_Start_Timestamp`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'Planned_Start_Timestamp' não possui skos:prefLabel em português (@pt-br)
- **`Planned_Start_Timestamp`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'Planned_Start_Timestamp' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
- **`PolymericLayerMaterialType`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'PolymericLayerMaterialType' não possui skos:definition em português (@pt-br)
- **`PostSlippingBendingStiffness`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'PostSlippingBendingStiffness' não possui skos:definition em português (@pt-br)
- **`PreSlippingBendingStiffness`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'PreSlippingBendingStiffness' não possui skos:definition em português (@pt-br)
- **`ProjectCode`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ProjectCode' não possui skos:definition em português (@pt-br)
- **`ProjectDrawingRevision`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ProjectDrawingRevision' não possui skos:definition em português (@pt-br)
- **`PullingHeadType`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'PullingHeadType' não possui skos:definition em português (@pt-br)
- **`Quantity`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'Quantity' não possui skos:definition em português (@pt-br)
- **`RingGasketAttribute`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'RingGasketAttribute' não possui dcterms:accessRights
- **`RingGasketAttribute`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'RingGasketAttribute' não possui skos:definition em inglês (@en)
- **`RingGasketAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'RingGasketAttribute' não possui skos:definition em português (@pt-br)
- **`RingGasketAttribute`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'RingGasketAttribute' não possui dcterms:identifier
- **`RingGasketAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'RingGasketAttribute' não possui skos:prefLabel em inglês (@en)
- **`RingGasketAttribute`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'RingGasketAttribute' não possui skos:prefLabel em português (@pt-br)
- **`RingGasketAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'RingGasketAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'RingGasketAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'RingGasketAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'RingGasketAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`RingGasketInnerDIameter`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'RingGasketInnerDIameter' não possui skos:definition em português (@pt-br)
- **`RingGasketMaterial`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'RingGasketMaterial' não possui skos:definition em português (@pt-br)
- **`RingGasketOuterDiameter`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'RingGasketOuterDiameter' não possui skos:definition em português (@pt-br)
- **`RingGasketPressureRating`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'RingGasketPressureRating' não possui skos:definition em português (@pt-br)
- **`RingGasketSpecification`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'RingGasketSpecification' não possui skos:definition em português (@pt-br)
- **`RingGasketStandard`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'RingGasketStandard' não possui skos:definition em português (@pt-br)
- **`RingGasketType`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'RingGasketType' não possui skos:definition em português (@pt-br)
- **`RiserConfiguration`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'RiserConfiguration' não possui skos:definition em português (@pt-br)
- **`RuptDefAlongFibers`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'RuptDefAlongFibers' não possui skos:definition em português (@pt-br)
- **`RuptDefPerpendFibers`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'RuptDefPerpendFibers' não possui skos:definition em português (@pt-br)
- **`SafeWorkingLoad`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'SafeWorkingLoad' não possui skos:definition em português (@pt-br)
- **`SerialNumber`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'SerialNumber' não possui skos:definition em português (@pt-br)
- **`ShackleInnerDiameter`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ShackleInnerDiameter' não possui skos:definition em português (@pt-br)
- **`ShackleOpeningWidth`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ShackleOpeningWidth' não possui skos:definition em português (@pt-br)
- **`ShackleOuterDiameter`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ShackleOuterDiameter' não possui skos:definition em português (@pt-br)
- **`ShackleThickness`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ShackleThickness' não possui skos:definition em português (@pt-br)
- **`SolubilityCurveAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'SolubilityCurveAttribute' não possui skos:definition em português (@pt-br)
- **`SolubilityCurveAttribute`** — `DOMAINATTR_IDENTIFIER_MISMATCH`
  - dcterms:identifier 'SolubilityTable' não corresponde ao local name 'SolubilityCurveAttribute'
- **`SolubilityCurveAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'SolubilityCurveAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'SolubilityCurveAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'SolubilityCurveAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`SolubilityTable_PolymerState`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'SolubilityTable_PolymerState' não possui skos:definition em português (@pt-br)
- **`SolubilityTable_SolubilityCoefficient`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'SolubilityTable_SolubilityCoefficient' não possui skos:definition em português (@pt-br)
- **`SolubilityTable_Temperature`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'SolubilityTable_Temperature' não possui skos:definition em português (@pt-br)
- **`SolubilityTableColumn`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'SolubilityTableColumn' não possui dcterms:accessRights
- **`SolubilityTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'SolubilityTableColumn' não possui skos:definition em inglês (@en)
- **`SolubilityTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'SolubilityTableColumn' não possui skos:definition em português (@pt-br)
- **`SolubilityTableColumn`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'SolubilityTableColumn' não possui dcterms:identifier
- **`SolubilityTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'SolubilityTableColumn' não possui skos:prefLabel em inglês (@en)
- **`SolubilityTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'SolubilityTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`SolubilityTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'SolubilityTableColumn' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'SolubilityTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'SolubilityTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'SolubilityTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`SpareQuantity`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'SpareQuantity' não possui skos:definition em português (@pt-br)
- **`SpoolingTension`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'SpoolingTension' não possui skos:definition em português (@pt-br)
- **`StrandsTable_SpareQuantity`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'StrandsTable_SpareQuantity' não possui skos:definition em português (@pt-br)
- **`StrandsTable_StrandsLength`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'StrandsTable_StrandsLength' não possui skos:definition em português (@pt-br)
- **`StrandsTable_StrandsQuantity`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'StrandsTable_StrandsQuantity' não possui skos:definition em português (@pt-br)
- **`StrandsTableAttribute`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'StrandsTableAttribute' não possui skos:definition em português (@pt-br)
- **`StrandsTableAttribute`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'StrandsTableAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'StrandsTableAttribute' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'StrandsTableAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`StrandsTableColumn`** — `DOMAINATTR_ACCESSRIGHTS_MISSING`
  - DomainAttribute 'StrandsTableColumn' não possui dcterms:accessRights
- **`StrandsTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_EN`
  - DomainAttribute 'StrandsTableColumn' não possui skos:definition em inglês (@en)
- **`StrandsTableColumn`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'StrandsTableColumn' não possui skos:definition em português (@pt-br)
- **`StrandsTableColumn`** — `DOMAINATTR_IDENTIFIER_MISSING`
  - DomainAttribute 'StrandsTableColumn' não possui dcterms:identifier
- **`StrandsTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_EN`
  - DomainAttribute 'StrandsTableColumn' não possui skos:prefLabel em inglês (@en)
- **`StrandsTableColumn`** — `DOMAINATTR_PREFLABEL_MISSING_PT_BR`
  - DomainAttribute 'StrandsTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`StrandsTableColumn`** — `DOMAINATTR_PROPERTY_MISSING`
  - DomainAttribute 'StrandsTableColumn' não possui propriedade obrigatória: edo:hasAttributeScope
  - DomainAttribute 'StrandsTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
  - DomainAttribute 'StrandsTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
  - DomainAttribute 'StrandsTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`StressAtDesignPressure`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'StressAtDesignPressure' não possui skos:definition em português (@pt-br)
- **`StrIntOffPLevMaxPressValRefMult`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'StrIntOffPLevMaxPressValRefMult' não possui skos:definition em português (@pt-br)
- **`StrIntOffPLevNomPressValRefMult`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'StrIntOffPLevNomPressValRefMult' não possui skos:definition em português (@pt-br)
- **`StrIntOnNoTensMaxPressValRefMult`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'StrIntOnNoTensMaxPressValRefMult' não possui skos:definition em português (@pt-br)
- **`StrIntOnNoTensNomPressValRefMult`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'StrIntOnNoTensNomPressValRefMult' não possui skos:definition em português (@pt-br)
- **`StructureCode`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'StructureCode' não possui skos:definition em português (@pt-br)
- **`SubProjectId`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'SubProjectId' não possui skos:definition em português (@pt-br)
- **`SupplierProvidedMaterialName`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'SupplierProvidedMaterialName' não possui skos:definition em português (@pt-br)
- **`TapesQuantity`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'TapesQuantity' não possui skos:definition em português (@pt-br)
- **`TechnicalNotes`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'TechnicalNotes' não possui skos:definition em português (@pt-br)
- **`TensileArmourFreeAnnulusVolume`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'TensileArmourFreeAnnulusVolume' não possui skos:definition em português (@pt-br)
- **`TensileWireLayAngle`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'TensileWireLayAngle' não possui skos:definition em português (@pt-br)
- **`TensileWiresCount`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'TensileWiresCount' não possui skos:definition em português (@pt-br)
- **`TensionerPadsOpeningAngle`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'TensionerPadsOpeningAngle' não possui skos:definition em português (@pt-br)
- **`ThreadPitch`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ThreadPitch' não possui skos:definition em português (@pt-br)
- **`ThreadsPerInch`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ThreadsPerInch' não possui skos:definition em português (@pt-br)
- **`ThreadStandard`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'ThreadStandard' não possui skos:definition em português (@pt-br)
- **`UltTensStrAlongFibers`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'UltTensStrAlongFibers' não possui skos:definition em português (@pt-br)
- **`UltTensStrPerpendFibers`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'UltTensStrPerpendFibers' não possui skos:definition em português (@pt-br)
- **`UnifilarDiagram`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'UnifilarDiagram' não possui skos:definition em português (@pt-br)
- **`UnifilarDiagramRev`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'UnifilarDiagramRev' não possui skos:definition em português (@pt-br)
- **`UpperItubeDiameter`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'UpperItubeDiameter' não possui skos:definition em português (@pt-br)
- **`UtilizationFactor`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'UtilizationFactor' não possui skos:definition em português (@pt-br)
- **`WireRopeQuantity`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'WireRopeQuantity' não possui skos:definition em português (@pt-br)
- **`WireRopeSlingLength`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'WireRopeSlingLength' não possui skos:definition em português (@pt-br)
- **`WorkingLoadLimit`** — `DOMAINATTR_DEFINITION_MISSING_PT_BR`
  - DomainAttribute 'WorkingLoadLimit' não possui skos:definition em português (@pt-br)

### 🏗️ Issues de Classes IFC

> **Formato de cada item:**
> - **`Nome da Entidade`** — `CÓDIGO_DO_ERRO`
>   - Descrição detalhada do problema encontrado

#### ❌ Erros Críticos (94)

- **`AbandonmentCap`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`AbandonmentCap`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`AbrasionProtector`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`AbrasionProtector`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`BendRestrictor`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`CommissioningActivity`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningActivity`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningContract`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningContract`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningDigitalProcessStep`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningDigitalProcessStep`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningEvidence`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningEvidence`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningIssue`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningIssue`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningItemCheck`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningItemCheck`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningLoopCheck`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningLoopCheck`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningPerson`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningPerson`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningPreservationOrder`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningPreservationOrder`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningProgram`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningProgram`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningProject`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningProject`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningResponsibleActor`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningResponsibleActor`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningResponsibleGroup`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningResponsibleGroup`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningTask`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningTask`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CompositeMaterial`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`DimensionsDrawing`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`DynamicUmbilicalSpan`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_equivalentClass
  - Classe IFC sem propriedade obrigatória: edo:ifc_objectType
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`ElectricalJumperConnector`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`ElectricalJumperConnector`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`ElectricalPowerJumperConnector`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`ElectricalPowerJumperConnector`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`Filler`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_equivalentClass
  - Classe IFC sem propriedade obrigatória: edo:ifc_objectType
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`FlangeAdapter`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`FlangeAdapter`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`FlangeConnection`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`FlowlineSpan`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_equivalentClass
  - Classe IFC sem propriedade obrigatória: edo:ifc_objectType
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`HotStab`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`HotStab`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`HotStabReceptacle`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`HotStabReceptacle`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`IfcInstanciableElement`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`IfcInstanciableElement`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`IntermediateBendStiffener`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`MetallicMaterial`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`PolymericMaterial`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`Project`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`Project`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_objectType
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`QuickConnectCoupling`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`QuickConnectCoupling`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`RigidJoint`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`RigidJoint`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`RiserSpan`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_equivalentClass
  - Classe IFC sem propriedade obrigatória: edo:ifc_objectType
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`StaticUmbilicalSpan`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_equivalentClass
  - Classe IFC sem propriedade obrigatória: edo:ifc_objectType
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`SubseaFlexiblePipesBsddDictionary`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`SubseaFlexiblePipesBsddDictionary`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`SubseaOilField`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`SubseaUmbilical`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`SubseaUmbilicalBsddDictionary`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`SubseaUmbilicalBsddDictionary`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`ThreadedFitting`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`ThreadedFitting`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`TopBendStiffener`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`UmbilicalBundle`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`UmbilicalLocation`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_equivalentClass
  - Classe IFC sem propriedade obrigatória: edo:ifc_objectType
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`UmbilicalPullingHead`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`UmbilicalPullingHead`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`UmbilicalStructure`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`WeldedConnection`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`WeldedConnection`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`WetChristmasTree`** — `IFC_BASE_CLASS_MISSING`
  - Classe IFC não herda de edo:IfcInstanciableElement
- **`WetChristmasTree`** — `IFC_REQUIRED_PROPERTY_MISSING`
  - Classe IFC sem propriedade obrigatória: edo:ifc_equivalentClass

### 📋 Issues Gerais (Classes/Propriedades)

> **Formato de cada item:**
> - **`Nome da Entidade`** — `CÓDIGO_DO_ERRO`
>   - Descrição detalhada do problema encontrado

#### ❌ Erros Críticos (166)

- **`AdministrativeAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'AdministrativeAttribute' não possui dcterms:identifier
- **`AnyURIType`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'AnyURIType' não possui dcterms:identifier
- **`ArchitecturalEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ArchitecturalEngineering' não possui dcterms:identifier
- **`AttributeClassification`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'AttributeClassification' não possui dcterms:identifier
- **`AttributeDomainCategory`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'AttributeDomainCategory' não possui dcterms:identifier
- **`AttributeNature`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'AttributeNature' não possui dcterms:identifier
- **`AttributeScope`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'AttributeScope' não possui dcterms:identifier
- **`AttributesGroup`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'AttributesGroup' não possui dcterms:identifier
- **`AttributeValueCardinality`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'AttributeValueCardinality' não possui dcterms:identifier
- **`AutomationControlEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'AutomationControlEngineering' não possui dcterms:identifier
- **`Base64BinaryType`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Base64BinaryType' não possui dcterms:identifier
- **`BasicDesign`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'BasicDesign' não possui dcterms:identifier
- **`BatchLevelAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'BatchLevelAttribute' não possui dcterms:identifier
- **`BendingStiffnessCurveAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'BendingStiffnessCurveAttribute' não possui dcterms:identifier
- **`BendingStiffnessTableColumn`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'BendingStiffnessTableColumn' não possui dcterms:identifier
- **`BendMomentVsShearForceCurveAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'BendMomentVsShearForceCurveAttribute' não possui dcterms:identifier
- **`BendMomentVsShearForceTableColumn`** — `CLASS_IDENTIFIER_MISMATCH`
  - dcterms:identifier 'BendMomentVsShearForceTable' não corresponde ao local name 'BendMomentVsShearForceTableColumn'
- **`Biomass`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Biomass' não possui dcterms:identifier
- **`BooleanValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'BooleanValue' não possui dcterms:identifier
- **`CalculatedValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'CalculatedValue' não possui dcterms:identifier
- **`CivilEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'CivilEngineering' não possui dcterms:identifier
- **`Commissioning`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Commissioning' não possui dcterms:identifier
- **`CommissioningElement`** — `CLASS_IDENTIFIER_MISMATCH`
  - dcterms:identifier 'CommissioningObject' não corresponde ao local name 'CommissioningElement'
- **`ComponentElement`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ComponentElement' não possui dcterms:identifier
- **`ConceptualDesign`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ConceptualDesign' não possui dcterms:identifier
- **`ConceptualMarker`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ConceptualMarker' não possui dcterms:identifier
- **`ConstructionPhase`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ConstructionPhase' não possui dcterms:identifier
- **`ConsumableElement`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ConsumableElement' não possui dcterms:identifier
- **`ContentManagementAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ContentManagementAttribute' não possui dcterms:identifier
- **`CrushingCurveAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'CrushingCurveAttribute' não possui dcterms:identifier
- **`CrushingFrictionCoefficientTighteningAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'CrushingFrictionCoefficientTighteningAttribute' não possui dcterms:identifier
- **`CrushingFrictionCoefficientTighteningTableColumn`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'CrushingFrictionCoefficientTighteningTableColumn' não possui dcterms:identifier
- **`CrushingMaximumAllowableTensionAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'CrushingMaximumAllowableTensionAttribute' não possui dcterms:identifier
- **`CrushingMaximumAllowableTensionTableColumn`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'CrushingMaximumAllowableTensionTableColumn' não possui dcterms:identifier
- **`CrushingMaximumAllowableTighteningAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'CrushingMaximumAllowableTighteningAttribute' não possui dcterms:identifier
- **`CrushingMaximumAllowableTighteningTableColumn`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'CrushingMaximumAllowableTighteningTableColumn' não possui dcterms:identifier
- **`DataType`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DataType' não possui dcterms:identifier
- **`DateTimeValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DateTimeValue' não possui dcterms:identifier
- **`DateValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DateValue' não possui dcterms:identifier
- **`DecimalValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DecimalValue' não possui dcterms:identifier
- **`DeclaredValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DeclaredValue' não possui dcterms:identifier
- **`Decommissioning`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Decommissioning' não possui dcterms:identifier
- **`DecommissioningPhase`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DecommissioningPhase' não possui dcterms:identifier
- **`DesignConditionAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DesignConditionAttribute' não possui dcterms:identifier
- **`DesignPhase`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DesignPhase' não possui dcterms:identifier
- **`DetailedDesign`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DetailedDesign' não possui dcterms:identifier
- **`DiffusionCurveAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DiffusionCurveAttribute' não possui dcterms:identifier
- **`DiffusionTableColumn`** — `CLASS_IDENTIFIER_MISMATCH`
  - dcterms:identifier 'DiffusionTable' não corresponde ao local name 'DiffusionTableColumn'
- **`DimensionalAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DimensionalAttribute' não possui dcterms:identifier
- **`DimensionsTableColumn`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DimensionsTableColumn' não possui dcterms:identifier
- **`Domain`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Domain' não possui dcterms:identifier
- **`DomainAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DomainAttribute' não possui dcterms:identifier
- **`DomainClassification`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DomainClassification' não possui dcterms:identifier
- **`DomainElement`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DomainElement' não possui dcterms:identifier
- **`DoubleValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DoubleValue' não possui dcterms:identifier
- **`Downstream`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Downstream' não possui dcterms:identifier
- **`DrawingDimensionsTableAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'DrawingDimensionsTableAttribute' não possui dcterms:identifier
- **`EarlyLeakMaxPressTableAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'EarlyLeakMaxPressTableAttribute' não possui dcterms:identifier
- **`EarlyLeakMaxPressTableColumn`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'EarlyLeakMaxPressTableColumn' não possui dcterms:identifier
- **`EarlyLeakNomPressTableAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'EarlyLeakNomPressTableAttribute' não possui dcterms:identifier
- **`EarlyLeakNomPressTableColumn`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'EarlyLeakNomPressTableColumn' não possui dcterms:identifier
- **`ElectricalEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ElectricalEngineering' não possui dcterms:identifier
- **`ElementClassification`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ElementClassification' não possui dcterms:identifier
- **`EModVsTempCurveAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'EModVsTempCurveAttribute' não possui dcterms:identifier
- **`EModVsTempTableColumn`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'EModVsTempTableColumn' não possui dcterms:identifier
- **`EnergyStorage`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'EnergyStorage' não possui dcterms:identifier
- **`EquipmentEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'EquipmentEngineering' não possui dcterms:identifier
- **`ExternalReference`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ExternalReference' não possui dcterms:identifier
- **`Fabrication`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Fabrication' não possui dcterms:identifier
- **`FabricationComponent`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'FabricationComponent' não possui dcterms:identifier
- **`FEED`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'FEED' não possui dcterms:identifier
- **`FinancialAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'FinancialAttribute' não possui dcterms:identifier
- **`FlangeAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'FlangeAttribute' não possui dcterms:identifier
- **`FlexibleStructure`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'FlexibleStructure' não possui dcterms:identifier
- **`FloatValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'FloatValue' não possui dcterms:identifier
- **`FunctionalAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'FunctionalAttribute' não possui dcterms:identifier
- **`Geothermal`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Geothermal' não possui dcterms:identifier
- **`HistoricalAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'HistoricalAttribute' não possui dcterms:identifier
- **`HVACEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'HVACEngineering' não possui dcterms:identifier
- **`HydrogenEnergy`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'HydrogenEnergy' não possui dcterms:identifier
- **`Hydropower`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Hydropower' não possui dcterms:identifier
- **`HydrostaticPressureTestsAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'HydrostaticPressureTestsAttribute' não possui dcterms:identifier
- **`IdentificationAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'IdentificationAttribute' não possui dcterms:identifier
- **`IfcInstanciableElement`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'IfcInstanciableElement' não possui dcterms:identifier
- **`ImportedValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ImportedValue' não possui dcterms:identifier
- **`Installation`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Installation' não possui dcterms:identifier
- **`InstanceLevelAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'InstanceLevelAttribute' não possui dcterms:identifier
- **`InstanciableElement`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'InstanciableElement' não possui dcterms:identifier
- **`InstrumentationEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'InstrumentationEngineering' não possui dcterms:identifier
- **`InternalIncidentalPressureCurveAttribute`** — `CLASS_IDENTIFIER_MISMATCH`
  - dcterms:identifier 'InternalIncidentalPressureTable' não corresponde ao local name 'InternalIncidentalPressureCurveAttribute'
- **`InternalIncidentalPressureTableColumn`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'InternalIncidentalPressureTableColumn' não possui dcterms:identifier
- **`IntValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'IntValue' não possui dcterms:identifier
- **`LayerGeometryAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'LayerGeometryAttribute' não possui dcterms:identifier
- **`LayingMinimumRadiusCurveAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'LayingMinimumRadiusCurveAttribute' não possui dcterms:identifier
- **`LayingMinimumRadiusTableColumn`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'LayingMinimumRadiusTableColumn' não possui dcterms:identifier
- **`LifecyclePhase`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'LifecyclePhase' não possui dcterms:identifier
- **`LocationType`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'LocationType' não possui dcterms:identifier
- **`LongValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'LongValue' não possui dcterms:identifier
- **`Maintenance`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Maintenance' não possui dcterms:identifier
- **`MaterialManufacturerAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'MaterialManufacturerAttribute' não possui dcterms:identifier
- **`MaterialType`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'MaterialType' não possui dcterms:identifier
- **`MaxDesignAbsIntPresCurveAttribute`** — `CLASS_IDENTIFIER_MISMATCH`
  - dcterms:identifier 'MaxDesignAbsIntPresTable' não corresponde ao local name 'MaxDesignAbsIntPresCurveAttribute'
- **`MaxDesignAbsIntPresTableColumn`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'MaxDesignAbsIntPresTableColumn' não possui dcterms:identifier
- **`MeasuredValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'MeasuredValue' não possui dcterms:identifier
- **`Midstream`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Midstream' não possui dcterms:identifier
- **`MultiValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'MultiValue' não possui dcterms:identifier
- **`Nuclear`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Nuclear' não possui dcterms:identifier
- **`NuclearFuelCycle`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'NuclearFuelCycle' não possui dcterms:identifier
- **`NuclearPowerGeneration`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'NuclearPowerGeneration' não possui dcterms:identifier
- **`Offshore`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Offshore' não possui dcterms:identifier
- **`OilAndGas`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'OilAndGas' não possui dcterms:identifier
- **`Onshore`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Onshore' não possui dcterms:identifier
- **`Operation`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Operation' não possui dcterms:identifier
- **`OperationPhase`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'OperationPhase' não possui dcterms:identifier
- **`PackageEquipmentEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'PackageEquipmentEngineering' não possui dcterms:identifier
- **`PartElement`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'PartElement' não possui dcterms:identifier
- **`PerformanceAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'PerformanceAttribute' não possui dcterms:identifier
- **`PermeabilityCurveAttribute`** — `CLASS_IDENTIFIER_MISMATCH`
  - dcterms:identifier 'PermeabilityTable' não corresponde ao local name 'PermeabilityCurveAttribute'
- **`PermeabilityTableColumn`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'PermeabilityTableColumn' não possui dcterms:identifier
- **`PhysicalPropertyAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'PhysicalPropertyAttribute' não possui dcterms:identifier
- **`Port`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Port' não possui dcterms:identifier
- **`PreCommissioning`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'PreCommissioning' não possui dcterms:identifier
- **`ProcessEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ProcessEngineering' não possui dcterms:identifier
- **`ProcessPipeSpec`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ProcessPipeSpec' não possui dcterms:identifier
- **`ProcessPipingEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ProcessPipingEngineering' não possui dcterms:identifier
- **`Procurement`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Procurement' não possui dcterms:identifier
- **`ProvenanceAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ProvenanceAttribute' não possui dcterms:identifier
- **`Recycling`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Recycling' não possui dcterms:identifier
- **`ReferenceDocument`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ReferenceDocument' não possui dcterms:identifier
- **`Renewable`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Renewable' não possui dcterms:identifier
- **`RingGasketAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'RingGasketAttribute' não possui dcterms:identifier
- **`RotatingEquipmentEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'RotatingEquipmentEngineering' não possui dcterms:identifier
- **`SafetyLossPreventionEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'SafetyLossPreventionEngineering' não possui dcterms:identifier
- **`SingleValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'SingleValue' não possui dcterms:identifier
- **`Solar`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Solar' não possui dcterms:identifier
- **`SolubilityCurveAttribute`** — `CLASS_IDENTIFIER_MISMATCH`
  - dcterms:identifier 'SolubilityTable' não corresponde ao local name 'SolubilityCurveAttribute'
- **`SolubilityTableColumn`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'SolubilityTableColumn' não possui dcterms:identifier
- **`SpatialAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'SpatialAttribute' não possui dcterms:identifier
- **`Specification`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Specification' não possui dcterms:identifier
- **`StaticEquipmentEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'StaticEquipmentEngineering' não possui dcterms:identifier
- **`Status`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Status' não possui dcterms:identifier
- **`StrandsTableColumn`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'StrandsTableColumn' não possui dcterms:identifier
- **`StringValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'StringValue' não possui dcterms:identifier
- **`StructuralEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'StructuralEngineering' não possui dcterms:identifier
- **`SubseaEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'SubseaEngineering' não possui dcterms:identifier
- **`SubseaFlexiblePipesEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'SubseaFlexiblePipesEngineering' não possui dcterms:identifier
- **`SubseaManifoldsEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'SubseaManifoldsEngineering' não possui dcterms:identifier
- **`SubseaRigidPipesEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'SubseaRigidPipesEngineering' não possui dcterms:identifier
- **`SubseaRigidPipeSpec`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'SubseaRigidPipeSpec' não possui dcterms:identifier
- **`SubseaStructuresEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'SubseaStructuresEngineering' não possui dcterms:identifier
- **`SubseaUmbilicalsEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'SubseaUmbilicalsEngineering' não possui dcterms:identifier
- **`Table`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Table' não possui dcterms:identifier
- **`TableColumn`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'TableColumn' não possui dcterms:identifier
- **`TechnicalDiscipline`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'TechnicalDiscipline' não possui dcterms:identifier
- **`ThermalPower`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ThermalPower' não possui dcterms:identifier
- **`TimeValue`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'TimeValue' não possui dcterms:identifier
- **`ToBeDeprecated`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ToBeDeprecated' não possui dcterms:identifier
- **`Transportation`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Transportation' não possui dcterms:identifier
- **`TypeLevelAttribute`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'TypeLevelAttribute' não possui dcterms:identifier
- **`Upstream`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Upstream' não possui dcterms:identifier
- **`UtilityPipingEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'UtilityPipingEngineering' não possui dcterms:identifier
- **`ValueNature`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ValueNature' não possui dcterms:identifier
- **`ValueOrigin`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'ValueOrigin' não possui dcterms:identifier
- **`Version`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Version' não possui dcterms:identifier
- **`WetChristmasTreesEngineering`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'WetChristmasTreesEngineering' não possui dcterms:identifier
- **`Wind`** — `CLASS_IDENTIFIER_MISSING`
  - Classe 'Wind' não possui dcterms:identifier

#### ⚠️ Avisos para Revisão (697)

- **`Accessory`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ActuatedEquipment`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ActuatedValve`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ActuatedValve`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Externally-actuated valve'@en não corresponde ao padrão esperado. Causa: palavra 'actuated' em 'Externally-actuated' deve começar com maiúscula
  - skos:prefLabel 'Válvula atuada externamente'@pt-br não corresponde ao padrão esperado. Causa: palavra 'atuada' deve começar com maiúscula (não é stopword)
- **`ActuatedValve`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Externally-actuated'→'Externally-Actuated', 'valve'→'Valve'; [pt-br] Title Case: 'atuada'→'Atuada', 'externamente'→'Externamente'
- **`Anchor`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`appliesTo`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ArmorPot`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`AssemblyTorque`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Torque de montagem'@pt-br não corresponde ao padrão esperado. Causa: palavra 'montagem' deve começar com maiúscula (não é stopword)
- **`AssemblyTorque`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'montagem'→'Montagem'
- **`Asset`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`AttributeDomainCategory`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`AttributeScope`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`AuxiliaryModule`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`AuxiliaryModule`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Auxiliary module'@en não corresponde ao padrão esperado. Causa: palavra 'module' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Módulo auxiliar'@pt-br não corresponde ao padrão esperado. Causa: palavra 'auxiliar' deve começar com maiúscula (não é stopword)
- **`AuxiliaryModule`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'module'→'Module'; [pt-br] Title Case: 'auxiliar'→'Auxiliar'
- **`AxialStiffnessUnderCompressionAtSeaLevel`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`AxialStiffnessUnderCompressionAtSeaLevel`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`AxialStiffnessUnderTensionAtSeaLevel`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`BatchLevelAttribute`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`BendMomentVsShearForceTable_BendingMoment`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Momento de flexão'@pt-br não corresponde ao padrão esperado. Causa: palavra 'flexão' deve começar com maiúscula (não é stopword)
- **`BendMomentVsShearForceTable_BendingMoment`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'flexão'→'Flexão'
- **`BendMomentVsShearForceTable_Condition`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Condição do flexível para os dados da curva'@pt-br não corresponde ao padrão esperado. Causa: palavra 'flexível' deve começar com maiúscula (não é stopword)
- **`BendMomentVsShearForceTable_Condition`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'flexível'→'Flexível', 'dados'→'Dados', 'curva'→'Curva'
- **`BendMomentVsShearForceTable_ShearForce`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`BendMomentVsShearForceTableColumn`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Bending moment vs Shear Force Table'@en não corresponde ao padrão esperado. Causa: palavra 'moment' deve começar com maiúscula (não é stopword)
- **`BendMomentVsShearForceTableColumn`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'moment'→'Moment'
- **`BlockValve`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`BlockValve`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Block valve'@en não corresponde ao padrão esperado. Causa: palavra 'valve' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Válvula de bloqueio'@pt-br não corresponde ao padrão esperado. Causa: palavra 'bloqueio' deve começar com maiúscula (não é stopword)
- **`BlockValve`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'valve'→'Valve'; [pt-br] Title Case: 'bloqueio'→'Bloqueio'
- **`BOP`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Blowout preventer'@en não corresponde ao padrão esperado. Causa: palavra 'preventer' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Blowout preventer'@pt-br não corresponde ao padrão esperado. Causa: palavra 'preventer' deve começar com maiúscula (não é stopword)
- **`BOP`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'preventer'→'Preventer'; [pt-br] Title Case: 'preventer'→'Preventer'
- **`BsddDataDictionary`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'BSDD'→'Bsdd'; [pt-br] Title Case: 'BSDD'→'Bsdd'
- **`BuoyancyTank`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Buoyancy tank'@en não corresponde ao padrão esperado. Causa: palavra 'tank' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Tanque de flutuação'@pt-br não corresponde ao padrão esperado. Causa: palavra 'flutuação' deve começar com maiúscula (não é stopword)
- **`BuoyancyTank`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'tank'→'Tank'; [pt-br] Title Case: 'flutuação'→'Flutuação'
- **`CalculatedValue`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`CarcassLayer`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`CasingHanger`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Casing hanger'@en não corresponde ao padrão esperado. Causa: palavra 'hanger' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Suspensor de revestimento'@pt-br não corresponde ao padrão esperado. Causa: palavra 'revestimento' deve começar com maiúscula (não é stopword)
- **`CasingHanger`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'hanger'→'Hanger'; [pt-br] Title Case: 'revestimento'→'Revestimento'
- **`ChainSegment`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Chain segment'@en não corresponde ao padrão esperado. Causa: palavra 'segment' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Tramo de corrente'@pt-br não corresponde ao padrão esperado. Causa: palavra 'corrente' deve começar com maiúscula (não é stopword)
- **`ChainSegment`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'segment'→'Segment'; [pt-br] Title Case: 'corrente'→'Corrente'
- **`CheckValve`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ChemicalInjectionUnit`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ChemicalInjectionUnit`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Chemical injection unit'@en não corresponde ao padrão esperado. Causa: palavra 'injection' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Unidade de injeção de químicos'@pt-br não corresponde ao padrão esperado. Causa: palavra 'injeção' deve começar com maiúscula (não é stopword)
- **`ChemicalInjectionUnit`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'injection'→'Injection', 'unit'→'Unit'; [pt-br] Title Case: 'injeção'→'Injeção', 'químicos'→'Químicos'
- **`ChokeModule`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ChokeModule`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Choke module'@en não corresponde ao padrão esperado. Causa: palavra 'module' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Módulo de choke'@pt-br não corresponde ao padrão esperado. Causa: palavra 'choke' deve começar com maiúscula (não é stopword)
- **`ChokeModule`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'module'→'Module'; [pt-br] Title Case: 'choke'→'Choke'
- **`ChokeValve`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ClampInternalDiameter`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final
- **`ClampInternalDiameter`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Diâmetro interno do clamp'@pt-br não corresponde ao padrão esperado. Causa: palavra 'interno' deve começar com maiúscula (não é stopword)
- **`ClampInternalDiameter`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'interno'→'Interno', 'clamp'→'Clamp'
- **`Component`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`ComponentDevice`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ConnectionModule`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ConnectionModule`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Connection module'@en não corresponde ao padrão esperado. Causa: palavra 'module' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Módulo de conexão'@pt-br não corresponde ao padrão esperado. Causa: palavra 'conexão' deve começar com maiúscula (não é stopword)
- **`ConnectionModule`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'module'→'Module'; [pt-br] Title Case: 'conexão'→'Conexão'
- **`CreatorId`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Creator Id'@en não corresponde ao padrão esperado. Causa: acrônimo 'Id' deve ser maiúsculo: ID
- **`CreatorId`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] acrônimos: ID
- **`CriticalCurvatureOfSlipping`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Curvatura crítica de escorregamento'@pt-br não corresponde ao padrão esperado. Causa: palavra 'crítica' deve começar com maiúscula (não é stopword)
- **`CriticalCurvatureOfSlipping`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Of'→'of'; [pt-br] Title Case: 'crítica'→'Crítica', 'escorregamento'→'Escorregamento'
- **`CrossoverModule`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`CrossoverModule`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Cross-over module'@en não corresponde ao padrão esperado. Causa: palavra 'over' em 'Cross-over' deve começar com maiúscula
  - skos:prefLabel 'Módulo de cross-over'@pt-br não corresponde ao padrão esperado. Causa: palavra 'cross' em 'cross-over' deve começar com maiúscula
- **`CrossoverModule`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Cross-over'→'Cross-Over', 'module'→'Module'; [pt-br] Title Case: 'cross-over'→'Cross-Over'
- **`DeclaredValue`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`DeploymentAccessory`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Acessório de lançamento'@pt-br não corresponde ao padrão esperado. Causa: palavra 'lançamento' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Deployment accessory'@en não corresponde ao padrão esperado. Causa: palavra 'accessory' deve começar com maiúscula (não é stopword)
- **`DeploymentAccessory`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'accessory'→'Accessory'; [pt-br] Title Case: 'lançamento'→'Lançamento'
- **`DiffusionTable_DiffusionCoefficient`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Coeficiente de difusão'@pt-br não corresponde ao padrão esperado. Causa: palavra 'difusão' deve começar com maiúscula (não é stopword)
- **`DiffusionTable_DiffusionCoefficient`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'difusão'→'Difusão'
- **`DiffusionTable_MoleculeIdentifier`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final; acrônimos em minúsculo: CH4, CO2, H2O, H2S
- **`DiffusionTable_PolymerState`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`DiffusionTableColumn`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`DimensionalAttribute`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`DimensioningCriteria`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`DistributionModule`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final
- **`DistributionModule`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Distribution module'@en não corresponde ao padrão esperado. Causa: palavra 'module' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Módulo de distribuição'@pt-br não corresponde ao padrão esperado. Causa: palavra 'distribuição' deve começar com maiúscula (não é stopword)
- **`DistributionModule`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'module'→'Module'; [pt-br] Title Case: 'distribuição'→'Distribuição'
- **`DragAnchor`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Drag anchor'@en não corresponde ao padrão esperado. Causa: palavra 'anchor' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Âncora de arrasto'@pt-br não corresponde ao padrão esperado. Causa: palavra 'arrasto' deve começar com maiúscula (não é stopword)
- **`DragAnchor`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'anchor'→'Anchor'; [pt-br] Title Case: 'arrasto'→'Arrasto'
- **`DrawingDimensionsTable_DimensionDescription`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`DrawingDimensionsTable_DimensionName`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Nome da dimensão'@pt-br não corresponde ao padrão esperado. Causa: palavra 'dimensão' deve começar com maiúscula (não é stopword)
- **`DrawingDimensionsTable_DimensionName`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'dimensão'→'Dimensão'
- **`DrawingDimensionsTable_DimensionValue`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Valor da dimensão'@pt-br não corresponde ao padrão esperado. Causa: palavra 'dimensão' deve começar com maiúscula (não é stopword)
- **`DrawingDimensionsTable_DimensionValue`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'dimensão'→'Dimensão'
- **`DynamicUmbilicalSpan`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`DynamicUmbilicalSpan`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Dynamic umbilical span'@en não corresponde ao padrão esperado. Causa: palavra 'umbilical' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Trecho dinâmico de umbilical'@pt-br não corresponde ao padrão esperado. Causa: palavra 'dinâmico' deve começar com maiúscula (não é stopword)
- **`DynamicUmbilicalSpan`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'umbilical'→'Umbilical', 'span'→'Span'; [pt-br] Title Case: 'dinâmico'→'Dinâmico', 'umbilical'→'Umbilical'
- **`EarlyLeakMaxPressTable_Press`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`EarlyLeakMaxPressTable_PressIntValStrat`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`EarlyLeakMaxPressTable_PressValRef`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`EarlyLeakMaxPressTable_PressValRefMult`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`EarlyLeakMaxPressTable_TensLimit`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`EarlyLeakNomPressTable_Press`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`EarlyLeakNomPressTable_PressIntValStrat`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`EarlyLeakNomPressTable_PressValRef`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`EarlyLeakNomPressTable_TensLimit`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`ElasticityModulusAt23Degrees`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`ElasticityModulusAt23Degrees`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`ElectricalCable`** — `MULTIPLE_PREFLABEL_SAME_LANG`
  - Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Cabo Elétrico', 'Cabo elétrico']
  - Classe tem 2 skos:prefLabel para idioma 'en': ['Electrical Cable', 'Electrical cable']
- **`ElectricalCable`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Cabo elétrico'@pt-br não corresponde ao padrão esperado. Causa: palavra 'elétrico' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Electrical cable'@en não corresponde ao padrão esperado. Causa: palavra 'cable' deve começar com maiúscula (não é stopword)
- **`ElectricalCable`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'cable'→'Cable'; [pt-br] Title Case: 'elétrico'→'Elétrico'
- **`ElectricalJumper`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ElectricalJumper`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Electrical jumper'@en não corresponde ao padrão esperado. Causa: palavra 'jumper' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Jumper elétrico'@pt-br não corresponde ao padrão esperado. Causa: palavra 'elétrico' deve começar com maiúscula (não é stopword)
- **`ElectricalJumper`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'jumper'→'Jumper'; [pt-br] Title Case: 'elétrico'→'Elétrico'
- **`ElectricalPowerJumper`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Electrical power jumper'@en não corresponde ao padrão esperado. Causa: palavra 'power' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Jumper elétrico de potência'@pt-br não corresponde ao padrão esperado. Causa: palavra 'elétrico' deve começar com maiúscula (não é stopword)
- **`ElectricalPowerJumper`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'power'→'Power', 'jumper'→'Jumper'; [pt-br] Title Case: 'elétrico'→'Elétrico', 'potência'→'Potência'
- **`ElectronicDevice`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Dispositivo eletrônico'@pt-br não corresponde ao padrão esperado. Causa: palavra 'eletrônico' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Electronic device'@en não corresponde ao padrão esperado. Causa: palavra 'device' deve começar com maiúscula (não é stopword)
- **`ElectronicDevice`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'device'→'Device'; [pt-br] Title Case: 'eletrônico'→'Eletrônico'
- **`EModVsTempTable_ElasticityModulus`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`EndFitting`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'End fitting'@en não corresponde ao padrão esperado. Causa: palavra 'fitting' deve começar com maiúscula (não é stopword)
- **`EndFitting`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'fitting'→'Fitting'
- **`Equipment`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`EquipmentLocation`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`ErosionalVelocity`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Velocidade erosional'@pt-br não corresponde ao padrão esperado. Causa: palavra 'erosional' deve começar com maiúscula (não é stopword)
- **`ErosionalVelocity`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'erosional'→'Erosional'
- **`ExecutiveProjectRevision`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`ExternalDiameter`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Diâmetro externo'@pt-br não corresponde ao padrão esperado. Causa: palavra 'externo' deve começar com maiúscula (não é stopword)
- **`ExternalDiameter`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'externo'→'Externo'
- **`FatMaxPress`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`FatMaxPressValRef`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`FatNomPress`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`FatNomPressValRef`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`FiberRopeSegment`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Fiber rope segment'@en não corresponde ao padrão esperado. Causa: palavra 'rope' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Tramo de cabo de fibra'@pt-br não corresponde ao padrão esperado. Causa: palavra 'cabo' deve começar com maiúscula (não é stopword)
- **`FiberRopeSegment`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'rope'→'Rope', 'segment'→'Segment'; [pt-br] Title Case: 'cabo'→'Cabo', 'fibra'→'Fibra'
- **`Filler`** — `MULTIPLE_PREFLABEL_SAME_LANG`
  - Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Enchimento', 'Preenchimento']
- **`FinancialAttribute`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`FlexibleStructure`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'FlexibleStructure'→'Flexiblestructure'
- **`FloatingProductionUnit`** — `ALTLABEL_TITLECASE_VIOLATION`
  - skos:altLabel 'FLNG'@en não segue Title Case
  - skos:altLabel 'FPSO'@en não segue Title Case
  - skos:altLabel 'FPU'@en não segue Title Case
- **`FloatingProductionUnit`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: '(UEP)'→'(uep)'
- **`FlowbaseRunningTool`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Ferramenta de instalação de BAP'@pt-br não corresponde ao padrão esperado. Causa: palavra 'instalação' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Flowbase running tool'@en não corresponde ao padrão esperado. Causa: palavra 'running' deve começar com maiúscula (não é stopword)
- **`FlowbaseRunningTool`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'running'→'Running', 'tool'→'Tool'; [pt-br] Title Case: 'instalação'→'Instalação'
- **`FlowConnector`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`FlowControlEquipment`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`FlowControlEquipment`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Equipamento de controle de fluxo'@pt-br não corresponde ao padrão esperado. Causa: palavra 'controle' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Flow control equipment'@en não corresponde ao padrão esperado. Causa: palavra 'control' deve começar com maiúscula (não é stopword)
- **`FlowControlEquipment`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'control'→'Control', 'equipment'→'Equipment'; [pt-br] Title Case: 'controle'→'Controle', 'fluxo'→'Fluxo'
- **`FlowControlModule`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`FlowControlModule`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Flow control module'@en não corresponde ao padrão esperado. Causa: palavra 'control' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Módulo de controle de fluxo'@pt-br não corresponde ao padrão esperado. Causa: palavra 'controle' deve começar com maiúscula (não é stopword)
- **`FlowControlModule`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'control'→'Control', 'module'→'Module'; [pt-br] Title Case: 'controle'→'Controle', 'fluxo'→'Fluxo'
- **`FlowLineMandrel`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`FlowLineMandrel`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Flow line mandrel'@en não corresponde ao padrão esperado. Causa: palavra 'line' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Mandril das linhas de fluxo'@pt-br não corresponde ao padrão esperado. Causa: palavra 'linhas' deve começar com maiúscula (não é stopword)
- **`FlowLineMandrel`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'line'→'Line', 'mandrel'→'Mandrel'; [pt-br] Title Case: 'linhas'→'Linhas', 'fluxo'→'Fluxo'
- **`FlowlineSpan`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`FlowlineSpan`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Flowline span'@en não corresponde ao padrão esperado. Causa: palavra 'span' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Trecho flowline'@pt-br não corresponde ao padrão esperado. Causa: palavra 'flowline' deve começar com maiúscula (não é stopword)
- **`FlowlineSpan`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'span'→'Span'; [pt-br] Title Case: 'flowline'→'Flowline'
- **`FrictionCoefBetweenPipeAndTensioner`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'And'→'and'
- **`FrictionCoefficientTighteningTable_CoefficientOfFriction`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Of'→'of'
- **`FrictionCoefficientTighteningTable_TighteningPerTrack`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Aperto por lagarta'@pt-br não corresponde ao padrão esperado. Causa: palavra 'lagarta' deve começar com maiúscula (não é stopword)
- **`FrictionCoefficientTighteningTable_TighteningPerTrack`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Per'→'per'; [pt-br] Title Case: 'lagarta'→'Lagarta'
- **`FSHRLowerAssembly`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Estrutura inferior de RHAS'@pt-br não corresponde ao padrão esperado. Causa: palavra 'inferior' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'FSHR lower assembly'@en não corresponde ao padrão esperado. Causa: palavra 'lower' deve começar com maiúscula (não é stopword)
- **`FSHRLowerAssembly`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'FSHR'→'Fshr', 'lower'→'Lower', 'assembly'→'Assembly'; [pt-br] Title Case: 'inferior'→'Inferior', 'RHAS'→'Rhas'
- **`FSHRUpperAssembly`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Estrutura de topo de RHAS'@pt-br não corresponde ao padrão esperado. Causa: palavra 'topo' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'FSHR upper assembly'@en não corresponde ao padrão esperado. Causa: palavra 'upper' deve começar com maiúscula (não é stopword)
- **`FSHRUpperAssembly`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'FSHR'→'Fshr', 'upper'→'Upper', 'assembly'→'Assembly'; [pt-br] Title Case: 'topo'→'Topo', 'RHAS'→'Rhas'
- **`FunctionalAttribute`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`FunctionLine`** — `MULTIPLE_PREFLABEL_SAME_LANG`
  - Classe tem 2 skos:prefLabel para idioma 'en': ['Function Line', 'Function line']
  - Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Linha Funcional', 'Linha de função']
- **`FunctionLine`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Function line'@en não corresponde ao padrão esperado. Causa: palavra 'line' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Linha de função'@pt-br não corresponde ao padrão esperado. Causa: palavra 'função' deve começar com maiúscula (não é stopword)
- **`FunctionLine`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'line'→'Line'; [pt-br] Title Case: 'função'→'Função'
- **`GroovePoint`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`GrooveSupportSurfaceDiameter`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Diâmetro da superfície de apoio do acessório'@pt-br não corresponde ao padrão esperado. Causa: palavra 'superfície' deve começar com maiúscula (não é stopword)
- **`GrooveSupportSurfaceDiameter`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'superfície'→'Superfície', 'apoio'→'Apoio', 'acessório'→'Acessório'
- **`GrooveSupportSurfaceFilletRadius`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`GrooveSupportSurfaceFilletRadius`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: '(Superfície'→'(superfície'
- **`GroutBag`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Grout bag'@en não corresponde ao padrão esperado. Causa: palavra 'bag' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Grout bag'@pt-br não corresponde ao padrão esperado. Causa: palavra 'bag' deve começar com maiúscula (não é stopword)
- **`GroutBag`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'bag'→'Bag'; [pt-br] Title Case: 'bag'→'Bag'
- **`GrvCntrPntDstnceFrmTermFlange`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final
- **`GrvCntrPntDstnceFrmTermFlange`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'From'→'from'
- **`GuideBase`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Base-guia'@pt-br não corresponde ao padrão esperado. Causa: palavra 'guia' em 'Base-guia' deve começar com maiúscula
  - skos:prefLabel 'Guide base'@en não corresponde ao padrão esperado. Causa: palavra 'base' deve começar com maiúscula (não é stopword)
- **`GuideBase`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'base'→'Base'; [pt-br] Title Case: 'Base-guia'→'Base-Guia'
- **`HangOffCollar`** — `ALTLABEL_TITLECASE_VIOLATION`
  - skos:altLabel 'Hang-Off Clamp'@en não segue Title Case
  - skos:altLabel 'Hang-Off Device'@en não segue Title Case
- **`HangOffCollar`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`hasAttribute`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`hasAttributeCategory`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`hasAttributeGroup`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`hasAttributeScope`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`hasDiscipline`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`hasDomain`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`hasLifecycleCreationPhase`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`hasLifecycleUsagePhase`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`hasLocationType`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`HasModaSensor`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'MODA'→'Moda'
- **`hasSubDomain`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`HasThermalInsulation`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Possui isolamento térmico'@pt-br não corresponde ao padrão esperado. Causa: palavra 'isolamento' deve começar com maiúscula (não é stopword)
- **`HasThermalInsulation`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'isolamento'→'Isolamento', 'térmico'→'Térmico'
- **`hasValueCardinality`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`HCM`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Horizontal connection module'@en não corresponde ao padrão esperado. Causa: palavra 'connection' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Módulo de conexão horizontal'@pt-br não corresponde ao padrão esperado. Causa: palavra 'conexão' deve começar com maiúscula (não é stopword)
- **`HCM`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'connection'→'Connection', 'module'→'Module'; [pt-br] Title Case: 'conexão'→'Conexão', 'horizontal'→'Horizontal'
- **`HCRHose`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final
- **`HCRHose`** — `MULTIPLE_DEFINITION`
  - Classe tem 2 skos:definition para idioma 'en' (máximo: 1)
- **`HistoricalAttribute`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`HPHousing`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Alojador de alta pressão'@pt-br não corresponde ao padrão esperado. Causa: palavra 'alta' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'High-pressure housing'@en não corresponde ao padrão esperado. Causa: palavra 'pressure' em 'High-pressure' deve começar com maiúscula
- **`HPHousing`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'High-pressure'→'High-Pressure', 'housing'→'Housing'; [pt-br] Title Case: 'alta'→'Alta', 'pressão'→'Pressão'
- **`Hub`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`HubBlockCap`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`HubBlockCap`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Capa de bloqueio de hub'@pt-br não corresponde ao padrão esperado. Causa: palavra 'bloqueio' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Hub block cap'@en não corresponde ao padrão esperado. Causa: palavra 'block' deve começar com maiúscula (não é stopword)
- **`HubBlockCap`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'block'→'Block', 'cap'→'Cap'; [pt-br] Title Case: 'bloqueio'→'Bloqueio', 'hub'→'Hub'
- **`HubProtectionCap`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`HubProtectionCap`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Capa de proteção de hub'@pt-br não corresponde ao padrão esperado. Causa: palavra 'proteção' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Hub protection cap'@en não corresponde ao padrão esperado. Causa: palavra 'protection' deve começar com maiúscula (não é stopword)
- **`HubProtectionCap`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'protection'→'Protection', 'cap'→'Cap'; [pt-br] Title Case: 'proteção'→'Proteção', 'hub'→'Hub'
- **`HydraulicJumper`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Hydraulic jumper'@en não corresponde ao padrão esperado. Causa: palavra 'jumper' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Jumper hidráulico'@pt-br não corresponde ao padrão esperado. Causa: palavra 'hidráulico' deve começar com maiúscula (não é stopword)
- **`HydraulicJumper`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'jumper'→'Jumper'; [pt-br] Title Case: 'hidráulico'→'Hidráulico'
- **`HydraulicPowerUnit`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`HydraulicPowerUnit`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Hydraulic power unit'@en não corresponde ao padrão esperado. Causa: palavra 'power' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Unidade de potência hidráulica'@pt-br não corresponde ao padrão esperado. Causa: palavra 'potência' deve começar com maiúscula (não é stopword)
- **`HydraulicPowerUnit`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'power'→'Power', 'unit'→'Unit'; [pt-br] Title Case: 'potência'→'Potência', 'hidráulica'→'Hidráulica'
- **`HydrostaticCollapseAbsPressDry`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`IdentificationAttribute`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`IdInUnifilarDiagram`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Id In Unifilar Diagram'@en não corresponde ao padrão esperado. Causa: acrônimo 'Id' deve ser maiúsculo: ID
- **`IdInUnifilarDiagram`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] acrônimos: ID
- **`ifc_equivalentClass`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ifc_objectType`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ifc_predefinedType`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ImportedValue`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`IMUX`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`IMUX`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'IWIS multiplexer'@en não corresponde ao padrão esperado. Causa: palavra 'multiplexer' deve começar com maiúscula (não é stopword)
- **`IMUX`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'IWIS'→'Iwis', 'multiplexer'→'Multiplexer'; [pt-br] Title Case: 'IWIS'→'Iwis'
- **`InlineT`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`InlineT`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel ''T' em linha'@pt-br não corresponde ao padrão esperado. Causa: formato não corresponde ao padrão Title Case esperado
  - skos:prefLabel ''T' em linha'@pt-br não corresponde ao padrão esperado. Causa: palavra 'linha' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Inline tee'@en não corresponde ao padrão esperado. Causa: palavra 'tee' deve começar com maiúscula (não é stopword)
- **`InlineT`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'tee'→'Tee'; [pt-br] Title Case: ''T''→''t'', 'linha'→'Linha'
- **`InlineValve`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Inline valve'@en não corresponde ao padrão esperado. Causa: palavra 'valve' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Válvula inline'@pt-br não corresponde ao padrão esperado. Causa: palavra 'inline' deve começar com maiúscula (não é stopword)
- **`InlineValve`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'valve'→'Valve'; [pt-br] Title Case: 'inline'→'Inline'
- **`InlineY`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`InlineY`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel ''Y' em linha'@pt-br não corresponde ao padrão esperado. Causa: formato não corresponde ao padrão Title Case esperado
  - skos:prefLabel ''Y' em linha'@pt-br não corresponde ao padrão esperado. Causa: palavra 'linha' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Inline wye'@en não corresponde ao padrão esperado. Causa: palavra 'wye' deve começar com maiúscula (não é stopword)
- **`InlineY`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'wye'→'Wye'; [pt-br] Title Case: ''Y''→''y'', 'linha'→'Linha'
- **`InstanceLevelAttribute`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`IntegratedPipe`** — `MULTIPLE_PREFLABEL_SAME_LANG`
  - Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Duto integrado', 'Tubo Integrado']
  - Classe tem 2 skos:prefLabel para idioma 'en': ['Integrated Pipe', 'Integrated pipe']
- **`IntegratedPipe`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Duto integrado'@pt-br não corresponde ao padrão esperado. Causa: palavra 'integrado' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Integrated pipe'@en não corresponde ao padrão esperado. Causa: palavra 'pipe' deve começar com maiúscula (não é stopword)
- **`IntegratedPipe`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'pipe'→'Pipe'; [pt-br] Title Case: 'integrado'→'Integrado'
- **`InternalDiameter`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Diâmetro interno'@pt-br não corresponde ao padrão esperado. Causa: palavra 'interno' deve começar com maiúscula (não é stopword)
- **`InternalDiameter`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'interno'→'Interno'
- **`InternalIncidentalPressureTable_PositionReference`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`InternalIncidentalPressureTable_VPosWRTWaterline`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'With'→'with', 'To'→'to'; [pt-br] Title Case: 'D'Água'→'d'Água'
- **`InternalVolume`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Volume interno'@pt-br não corresponde ao padrão esperado. Causa: palavra 'interno' deve começar com maiúscula (não é stopword)
- **`InternalVolume`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'interno'→'Interno'
- **`IsSpare`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'É um sobressalente'@pt-br não corresponde ao padrão esperado. Causa: palavra 'sobressalente' deve começar com maiúscula (não é stopword)
- **`IsSpare`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'sobressalente'→'Sobressalente'
- **`ITube`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'I-tube'@en não corresponde ao padrão esperado. Causa: acrônimo 'I-tube' deve ser maiúsculo: I-TUBE
  - skos:prefLabel 'I-tube'@pt-br não corresponde ao padrão esperado. Causa: acrônimo 'I-tube' deve ser maiúsculo: I-TUBE
- **`ITube`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] acrônimos: TUBE; [pt-br] acrônimos: TUBE
- **`Jumper`** — `ALTLABEL_TITLECASE_VIOLATION`
  - skos:altLabel 'Flying lead'@en não segue Title Case
- **`Jumper`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`Jumper`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Jumper de controle/sinal'@pt-br não corresponde ao padrão esperado. Causa: palavra 'controle/sinal' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Signal/control jumper'@en não corresponde ao padrão esperado. Causa: palavra 'jumper' deve começar com maiúscula (não é stopword)
- **`Jumper`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'jumper'→'Jumper'; [pt-br] Title Case: 'controle/sinal'→'Controle/sinal'
- **`LayerAnnular`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`LayerAnnularType`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`LayerContinuity`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`LayerGeometryInertiaY`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Inércia  Y da Geometria da Camada'@pt-br não corresponde ao padrão esperado. Causa: contém espaços múltiplos consecutivos
- **`LayerGeometryInertiaY`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] formatação de texto
- **`LayerThickness`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Espessura da camada'@pt-br não corresponde ao padrão esperado. Causa: palavra 'camada' deve começar com maiúscula (não é stopword)
- **`LayerThickness`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'camada'→'Camada'
- **`LayingMinimumRadiusTable_AbsoluteExternalPressure`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Pressão Externa absoluta'@pt-br não corresponde ao padrão esperado. Causa: palavra 'absoluta' deve começar com maiúscula (não é stopword)
- **`LayingMinimumRadiusTable_AbsoluteExternalPressure`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'absoluta'→'Absoluta'
- **`LayingMinimumRadiusTable_AbsoluteInternalPressure`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Pressão interna absoluta'@pt-br não corresponde ao padrão esperado. Causa: palavra 'interna' deve começar com maiúscula (não é stopword)
- **`LayingMinimumRadiusTable_AbsoluteInternalPressure`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'interna'→'Interna', 'absoluta'→'Absoluta'
- **`LayingMinimumRadiusTable_SectionSupportedByRigidSupport`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'By'→'by'
- **`LayingMinimumRadiusTable_TensileArmourAnnulusCondition`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`LimpTorsionalStiffnessAtSeaLevel`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`LimpTorsionalStiffnessAtSeaLevel`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`LinearLocation`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`LinearObject`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`LineSpan`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`LineSpan`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Line span'@en não corresponde ao padrão esperado. Causa: palavra 'span' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Trecho de linha'@pt-br não corresponde ao padrão esperado. Causa: palavra 'linha' deve começar com maiúscula (não é stopword)
- **`LineSpan`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'span'→'Span'; [pt-br] Title Case: 'linha'→'Linha'
- **`LineTermination`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`LineTerminationModule`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Line termination module'@en não corresponde ao padrão esperado. Causa: palavra 'termination' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Módulo de terminação de linha'@pt-br não corresponde ao padrão esperado. Causa: palavra 'terminação' deve começar com maiúscula (não é stopword)
- **`LineTerminationModule`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'termination'→'Termination', 'module'→'Module'; [pt-br] Title Case: 'terminação'→'Terminação', 'linha'→'Linha'
- **`Location`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`LogicalElement`** — `MULTIPLE_DEFINITION`
  - Classe tem 2 skos:definition para idioma 'pt-br' (máximo: 1)
  - Classe tem 2 skos:definition para idioma 'en' (máximo: 1)
- **`LogicCap`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Capa lógica'@pt-br não corresponde ao padrão esperado. Causa: palavra 'lógica' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Logic cap'@en não corresponde ao padrão esperado. Causa: palavra 'cap' deve começar com maiúscula (não é stopword)
- **`LogicCap`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'cap'→'Cap'; [pt-br] Title Case: 'lógica'→'Lógica'
- **`LongTermFloatDensity`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`LPHousing`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Alojador de baixa pressão'@pt-br não corresponde ao padrão esperado. Causa: palavra 'baixa' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Low-pressure housing'@en não corresponde ao padrão esperado. Causa: palavra 'pressure' em 'Low-pressure' deve começar com maiúscula
- **`LPHousing`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Low-pressure'→'Low-Pressure', 'housing'→'Housing'; [pt-br] Title Case: 'baixa'→'Baixa', 'pressão'→'Pressão'
- **`LubricantFrictionFactor`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Fator de atrito do lubrificante'@pt-br não corresponde ao padrão esperado. Causa: palavra 'atrito' deve começar com maiúscula (não é stopword)
- **`LubricantFrictionFactor`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'atrito'→'Atrito', 'lubrificante'→'Lubrificante'
- **`Manifold`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ManufacturerDefinedMaterialName`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Nome do material conforme designado pelo fabricante do item final'@pt-br não corresponde ao padrão esperado. Causa: palavra 'material' deve começar com maiúscula (não é stopword)
- **`ManufacturerDefinedMaterialName`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'material'→'Material', 'conforme'→'Conforme', 'designado'→'Designado'
- **`MasterControlStation`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`MasterControlStation`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Estação de controle mestra'@pt-br não corresponde ao padrão esperado. Causa: palavra 'controle' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Master control station'@en não corresponde ao padrão esperado. Causa: palavra 'control' deve começar com maiúscula (não é stopword)
- **`MasterControlStation`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'control'→'Control', 'station'→'Station'; [pt-br] Title Case: 'controle'→'Controle', 'mestra'→'Mestra'
- **`MaterialRequest`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: '(RM)'→'(rm)'
- **`MaterialRequestRev`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: '(RM)'→'(rm)'
- **`MaterialSupplierName`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Nome da empresa responsável por fornecer o material'@pt-br não corresponde ao padrão esperado. Causa: palavra 'empresa' deve começar com maiúscula (não é stopword)
- **`MaterialSupplierName`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'empresa'→'Empresa', 'responsável'→'Responsável', 'fornecer'→'Fornecer'
- **`Mattress`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`MaxDesignAbsIntPresTable_PositionReference`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`MaxDesignAbsIntPresTable_VPosWRTWaterline`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'With'→'with', 'To'→'to'; [pt-br] Title Case: 'D'Água'→'d'Água'
- **`MaxDynamicLoad`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: '(MDL)'→'(mdl)'; [pt-br] Title Case: '(MDL)'→'(mdl)'
- **`MaximumAllowableTensileForStraightLine`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'For'→'for'
- **`MaximumAllowableTighteningTable_TighteningPerTrack`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Per'→'per'
- **`MaximumAmbientTemperature`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Temperatura ambiente máxima'@pt-br não corresponde ao padrão esperado. Causa: palavra 'ambiente' deve começar com maiúscula (não é stopword)
- **`MaximumAmbientTemperature`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'ambiente'→'Ambiente', 'máxima'→'Máxima'
- **`MaximumThermalExchangeCoefficient`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: '(TEC)'→'(tec)'; [pt-br] Title Case: '(TEC)'→'(tec)'
- **`MaxPermissibleDeformationDynamic`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`MaxPermissibleDeformationStatic`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`MeasuredValue`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`MetallicStrandLength`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final
- **`MetallicTubing`** — `MULTIPLE_PREFLABEL_SAME_LANG`
  - Classe tem 2 skos:prefLabel para idioma 'en': ['Metallic Tubing', 'Metallic tubing']
  - Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Tubulação Metálica', 'Tubulação metálica']
- **`MetallicTubing`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Metallic tubing'@en não corresponde ao padrão esperado. Causa: palavra 'tubing' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Tubulação metálica'@pt-br não corresponde ao padrão esperado. Causa: palavra 'metálica' deve começar com maiúscula (não é stopword)
- **`MetallicTubing`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'tubing'→'Tubing'; [pt-br] Title Case: 'metálica'→'Metálica'
- **`MinimumBendingRadiusForStorage`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'For'→'for'
- **`MinimumTemperature`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final
- **`MinimumThermalExchangeCoefficient`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: '(TEC)'→'(tec)'; [pt-br] Title Case: '(TEC)'→'(tec)'
- **`ModulusOfElasticity`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Módulo de elasticidade'@pt-br não corresponde ao padrão esperado. Causa: palavra 'elasticidade' deve começar com maiúscula (não é stopword)
- **`ModulusOfElasticity`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Of'→'of'; [pt-br] Title Case: 'elasticidade'→'Elasticidade'
- **`NumberOfChokeValves`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`NumberOfChokeValves`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Número de válvulas de estrangulamento'@pt-br não corresponde ao padrão esperado. Causa: palavra 'válvulas' deve começar com maiúscula (não é stopword)
- **`NumberOfChokeValves`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Of'→'of'; [pt-br] Title Case: 'válvulas'→'Válvulas', 'estrangulamento'→'Estrangulamento'
- **`NumberOfRemoteProcessIsolationValves`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`NumberOfRemoteProcessIsolationValves`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Número de válvulas de isolamento de processo remoto'@pt-br não corresponde ao padrão esperado. Causa: palavra 'válvulas' deve começar com maiúscula (não é stopword)
- **`NumberOfRemoteProcessIsolationValves`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Of'→'of'; [pt-br] Title Case: 'válvulas'→'Válvulas', 'isolamento'→'Isolamento', 'processo'→'Processo'
- **`OffLeakPLevMaxPress`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`OffLeakPLevMaxPress`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`OffLeakPLevMaxPressValRef`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`OffLeakPLevMaxPressValRef`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`OffLeakPLevMaxPressValRefMult`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`OffLeakPLevNomPress`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`OffLeakPLevNomPress`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`OffLeakPLevNomPressValRef`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`OffLeakPLevNomPressValRef`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`OffLeakPLevNomPressValRefMult`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`OpenReceptacle`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Open receptacle'@en não corresponde ao padrão esperado. Causa: palavra 'receptacle' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Receptáculo aberto'@pt-br não corresponde ao padrão esperado. Causa: palavra 'aberto' deve começar com maiúscula (não é stopword)
- **`OpenReceptacle`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'receptacle'→'Receptacle'; [pt-br] Title Case: 'aberto'→'Aberto'
- **`OpticalFiberCable`** — `MULTIPLE_PREFLABEL_SAME_LANG`
  - Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Cabo de Fibra Óptica', 'Cabo de fibra ótica']
  - Classe tem 2 skos:prefLabel para idioma 'en': ['Optical Fiber Cable', 'Optical fiber cable']
- **`OpticalFiberCable`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Cabo de fibra ótica'@pt-br não corresponde ao padrão esperado. Causa: palavra 'fibra' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Optical fiber cable'@en não corresponde ao padrão esperado. Causa: palavra 'fiber' deve começar com maiúscula (não é stopword)
- **`OpticalFiberCable`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'fiber'→'Fiber', 'cable'→'Cable'; [pt-br] Title Case: 'fibra'→'Fibra', 'ótica'→'Ótica'
- **`OuterDiameter`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Diâmetro externo'@pt-br não corresponde ao padrão esperado. Causa: palavra 'externo' deve começar com maiúscula (não é stopword)
- **`OuterDiameter`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'externo'→'Externo'
- **`PartNumber`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Número da peça do acessório'@pt-br não corresponde ao padrão esperado. Causa: palavra 'peça' deve começar com maiúscula (não é stopword)
- **`PartNumber`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'peça'→'Peça', 'acessório'→'Acessório'
- **`PerformanceAttribute`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`PermeabilityCurveAttribute`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`PermeabilityTable_MoleculeIdentifier`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final; acrônimos em minúsculo: CH4, CO2, H2O, H2S
- **`PermeabilityTable_PolymerState`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`PhysicalConnection`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`PhysicalPropertyAttribute`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`Piggable`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`PipelineSpan`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`PipelineSpan`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Pipeline span'@en não corresponde ao padrão esperado. Causa: palavra 'span' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Trecho de duto'@pt-br não corresponde ao padrão esperado. Causa: palavra 'duto' deve começar com maiúscula (não é stopword)
- **`PipelineSpan`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'span'→'Span'; [pt-br] Title Case: 'duto'→'Duto'
- **`PipeSectionApplication`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`PipeSegment`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`PipingSpool`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`PipingSpool`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Piping spool'@en não corresponde ao padrão esperado. Causa: palavra 'spool' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Trecho de tubulação'@pt-br não corresponde ao padrão esperado. Causa: palavra 'tubulação' deve começar com maiúscula (não é stopword)
- **`PipingSpool`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'spool'→'Spool'; [pt-br] Title Case: 'tubulação'→'Tubulação'
- **`PlasticHose`** — `MULTIPLE_PREFLABEL_SAME_LANG`
  - Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Mangueira Plástica', 'Mangueira plástica']
- **`PlasticHose`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Mangueira plástica'@pt-br não corresponde ao padrão esperado. Causa: palavra 'plástica' deve começar com maiúscula (não é stopword)
- **`PlasticHose`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'plástica'→'Plástica'
- **`PLEM`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`PLET`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`PointLocation`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`PoissonRatioAt23Degrees`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`PoissonRatioAt23Degrees`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`PowerMachine`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`PowerMachine`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Máquina de potência'@pt-br não corresponde ao padrão esperado. Causa: palavra 'potência' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Power machine'@en não corresponde ao padrão esperado. Causa: palavra 'machine' deve começar com maiúscula (não é stopword)
- **`PowerMachine`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'machine'→'Machine'; [pt-br] Title Case: 'potência'→'Potência'
- **`PressureComponent`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Component de contenção de pressão'@pt-br não corresponde ao padrão esperado. Causa: palavra 'contenção' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Pressure-containing component'@en não corresponde ao padrão esperado. Causa: palavra 'containing' em 'Pressure-containing' deve começar com maiúscula
- **`PressureComponent`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Pressure-containing'→'Pressure-Containing', 'component'→'Component'; [pt-br] Title Case: 'contenção'→'Contenção', 'pressão'→'Pressão'
- **`PressureEquipment`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`PressureEquipment`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Equipamentos de contenção de pressão'@pt-br não corresponde ao padrão esperado. Causa: palavra 'contenção' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Pressure-containing equipment'@en não corresponde ao padrão esperado. Causa: palavra 'containing' em 'Pressure-containing' deve começar com maiúscula
- **`PressureEquipment`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Pressure-containing'→'Pressure-Containing', 'equipment'→'Equipment'; [pt-br] Title Case: 'contenção'→'Contenção', 'pressão'→'Pressão'
- **`PressureSensor`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Pressure sensor'@en não corresponde ao padrão esperado. Causa: palavra 'sensor' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Sensor de pressão'@pt-br não corresponde ao padrão esperado. Causa: palavra 'pressão' deve começar com maiúscula (não é stopword)
- **`PressureSensor`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'sensor'→'Sensor'; [pt-br] Title Case: 'pressão'→'Pressão'
- **`ProcessingModule`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ProcessingModule`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Módulo de processamento'@pt-br não corresponde ao padrão esperado. Causa: palavra 'processamento' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Processing module'@en não corresponde ao padrão esperado. Causa: palavra 'module' deve começar com maiúscula (não é stopword)
- **`ProcessingModule`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'module'→'Module'; [pt-br] Title Case: 'processamento'→'Processamento'
- **`ProjectAcronym`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`ProjectCode`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Código Identificador único do projeto da operadora da Interligação Submarina'@pt-br não corresponde ao padrão esperado. Causa: palavra 'único' deve começar com maiúscula (não é stopword)
- **`ProjectCode`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'único'→'Único', 'projeto'→'Projeto', 'operadora'→'Operadora'
- **`ProjectDrawingCode`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`PullInCollar`** — `ALTLABEL_TITLECASE_VIOLATION`
  - skos:altLabel 'Pull-In Clamp'@en não segue Title Case
- **`PumpingModule`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`PumpingModule`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Módulo de bombeamento'@pt-br não corresponde ao padrão esperado. Causa: palavra 'bombeamento' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Pumping module'@en não corresponde ao padrão esperado. Causa: palavra 'module' deve começar com maiúscula (não é stopword)
- **`PumpingModule`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'module'→'Module'; [pt-br] Title Case: 'bombeamento'→'Bombeamento'
- **`QuickDisconnectionTool`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Ferramenta de desconexão rápida'@pt-br não corresponde ao padrão esperado. Causa: palavra 'desconexão' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Quick disconnection tool'@en não corresponde ao padrão esperado. Causa: palavra 'disconnection' deve começar com maiúscula (não é stopword)
- **`QuickDisconnectionTool`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'disconnection'→'Disconnection', 'tool'→'Tool'; [pt-br] Title Case: 'desconexão'→'Desconexão', 'rápida'→'Rápida'
- **`ReliefValve`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ReliefValve`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Relief valve'@en não corresponde ao padrão esperado. Causa: palavra 'valve' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Válvula de alívio'@pt-br não corresponde ao padrão esperado. Causa: palavra 'alívio' deve começar com maiúscula (não é stopword)
- **`ReliefValve`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'valve'→'Valve'; [pt-br] Title Case: 'alívio'→'Alívio'
- **`RigidJumper`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`RigidJumper`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Jumper rígido'@pt-br não corresponde ao padrão esperado. Causa: palavra 'rígido' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Rigid jumper'@en não corresponde ao padrão esperado. Causa: palavra 'jumper' deve começar com maiúscula (não é stopword)
- **`RigidJumper`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'jumper'→'Jumper'; [pt-br] Title Case: 'rígido'→'Rígido'
- **`RingGasket`** — `ALTLABEL_TITLECASE_VIOLATION`
  - skos:altLabel ' Seal Ring'@en não segue Title Case
  - skos:altLabel 'O-Ring'@en não segue Title Case
- **`RiserBalcony`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`RiserSpan`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`RiserSpan`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Riser span'@en não corresponde ao padrão esperado. Causa: palavra 'span' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Trecho riser'@pt-br não corresponde ao padrão esperado. Causa: palavra 'riser' deve começar com maiúscula (não é stopword)
- **`RiserSpan`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'span'→'Span'; [pt-br] Title Case: 'riser'→'Riser'
- **`RiserSupport`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`RiserSupport`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Riser support'@en não corresponde ao padrão esperado. Causa: palavra 'support' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Suporte de riser'@pt-br não corresponde ao padrão esperado. Causa: palavra 'riser' deve começar com maiúscula (não é stopword)
- **`RiserSupport`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'support'→'Support'; [pt-br] Title Case: 'riser'→'Riser'
- **`RiserSupportBuoy`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Bóia de sustentação de risers'@pt-br não corresponde ao padrão esperado. Causa: palavra 'sustentação' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Riser support buoy'@en não corresponde ao padrão esperado. Causa: palavra 'support' deve começar com maiúscula (não é stopword)
- **`RiserSupportBuoy`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'support'→'Support', 'buoy'→'Buoy'; [pt-br] Title Case: 'sustentação'→'Sustentação', 'risers'→'Risers'
- **`RoboticActuator`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`RoboticActuator`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Atuador robótico'@pt-br não corresponde ao padrão esperado. Causa: palavra 'robótico' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Robotic actuator'@en não corresponde ao padrão esperado. Causa: palavra 'actuator' deve começar com maiúscula (não é stopword)
- **`RoboticActuator`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'actuator'→'Actuator'; [pt-br] Title Case: 'robótico'→'Robótico'
- **`RopeSegment`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Rope segment'@en não corresponde ao padrão esperado. Causa: palavra 'segment' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Tramo de cabo'@pt-br não corresponde ao padrão esperado. Causa: palavra 'cabo' deve começar com maiúscula (não é stopword)
- **`RopeSegment`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'segment'→'Segment'; [pt-br] Title Case: 'cabo'→'Cabo'
- **`RotatingMachine`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Máquina rotativa'@pt-br não corresponde ao padrão esperado. Causa: palavra 'rotativa' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Rotating machine'@en não corresponde ao padrão esperado. Causa: palavra 'machine' deve começar com maiúscula (não é stopword)
- **`RotatingMachine`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'machine'→'Machine'; [pt-br] Title Case: 'rotativa'→'Rotativa'
- **`ROVTool`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final
- **`ROVTool`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'ROV tool'@en não corresponde ao padrão esperado. Causa: palavra 'tool' deve começar com maiúscula (não é stopword)
- **`ROVTool`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'tool'→'Tool'
- **`RunningTool`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`RunningTool`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Ferramenta submarina de instalação'@pt-br não corresponde ao padrão esperado. Causa: palavra 'submarina' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Subsea running tool'@en não corresponde ao padrão esperado. Causa: palavra 'running' deve começar com maiúscula (não é stopword)
- **`RunningTool`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'running'→'Running', 'tool'→'Tool'; [pt-br] Title Case: 'submarina'→'Submarina', 'instalação'→'Instalação'
- **`RunOfRiver`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Hidrelétrica a Fio d’Água'@pt-br não corresponde ao padrão esperado. Causa: contém caracteres inválidos: ['’']
  - skos:prefLabel 'Hidrelétrica a Fio d’Água'@pt-br não corresponde ao padrão esperado. Causa: palavra 'd’Água' deve começar com maiúscula (não é stopword)
- **`RunOfRiver`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Run-of-River'→'Run-Of-River'; [pt-br] Title Case: 'd’Água'→'D’água'
- **`RuptDefAlongFibers`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Deformação de Ruptura longitudinalmente às fibras'@pt-br não corresponde ao padrão esperado. Causa: palavra 'longitudinalmente' deve começar com maiúscula (não é stopword)
- **`RuptDefAlongFibers`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'longitudinalmente'→'Longitudinalmente', 'fibras'→'Fibras'
- **`RuptDefPerpendFibers`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Deformação de Ruptura perpendicularmente às fibras'@pt-br não corresponde ao padrão esperado. Causa: palavra 'perpendicularmente' deve começar com maiúscula (não é stopword)
- **`RuptDefPerpendFibers`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'To'→'to'; [pt-br] Title Case: 'perpendicularmente'→'Perpendicularmente', 'fibras'→'Fibras'
- **`SandDetector`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Detector de areia'@pt-br não corresponde ao padrão esperado. Causa: palavra 'areia' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Sand detector'@en não corresponde ao padrão esperado. Causa: palavra 'detector' deve começar com maiúscula (não é stopword)
- **`SandDetector`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'detector'→'Detector'; [pt-br] Title Case: 'areia'→'Areia'
- **`SCM`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`SCM`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Módulo de controle submarino'@pt-br não corresponde ao padrão esperado. Causa: palavra 'controle' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Subsea control module'@en não corresponde ao padrão esperado. Causa: palavra 'control' deve começar com maiúscula (não é stopword)
- **`SCM`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'control'→'Control', 'module'→'Module'; [pt-br] Title Case: 'controle'→'Controle', 'submarino'→'Submarino'
- **`SCMMB`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`SCMMB`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Base de montagem de SCM'@pt-br não corresponde ao padrão esperado. Causa: palavra 'montagem' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'SCM mounting base'@en não corresponde ao padrão esperado. Causa: palavra 'mounting' deve começar com maiúscula (não é stopword)
- **`SCMMB`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'mounting'→'Mounting', 'base'→'Base'; [pt-br] Title Case: 'montagem'→'Montagem'
- **`SCMRunningTool`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Ferramenta de instalação de SCM'@pt-br não corresponde ao padrão esperado. Causa: palavra 'instalação' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'SCM running tool'@en não corresponde ao padrão esperado. Causa: palavra 'running' deve começar com maiúscula (não é stopword)
- **`SCMRunningTool`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'running'→'Running', 'tool'→'Tool'; [pt-br] Title Case: 'instalação'→'Instalação'
- **`SDU`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Subsea distribution unit'@en não corresponde ao padrão esperado. Causa: palavra 'distribution' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Unidade de distribuição submarina'@pt-br não corresponde ao padrão esperado. Causa: palavra 'distribuição' deve começar com maiúscula (não é stopword)
- **`SDU`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'distribution'→'Distribution', 'unit'→'Unit'; [pt-br] Title Case: 'distribuição'→'Distribuição', 'submarina'→'Submarina'
- **`SEM`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Módulo eletrônico submarino'@pt-br não corresponde ao padrão esperado. Causa: palavra 'eletrônico' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Subsea electronic module'@en não corresponde ao padrão esperado. Causa: palavra 'electronic' deve começar com maiúscula (não é stopword)
- **`SEM`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'electronic'→'Electronic', 'module'→'Module'; [pt-br] Title Case: 'eletrônico'→'Eletrônico', 'submarino'→'Submarino'
- **`SeparatorVessel`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Seaparator vessel'@en não corresponde ao padrão esperado. Causa: palavra 'vessel' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Vaso separador'@pt-br não corresponde ao padrão esperado. Causa: palavra 'separador' deve começar com maiúscula (não é stopword)
- **`SeparatorVessel`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'vessel'→'Vessel'; [pt-br] Title Case: 'separador'→'Separador'
- **`Service`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`Shackle`** — `ALTLABEL_TITLECASE_VIOLATION`
  - skos:altLabel 'D-Shackle'@en não segue Title Case
  - skos:altLabel 'U-Bolt'@en não segue Title Case
- **`Shackle`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`ShackleInnerDiameter`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Diâmetro interno da furação do olhal'@pt-br não corresponde ao padrão esperado. Causa: palavra 'interno' deve começar com maiúscula (não é stopword)
- **`ShackleInnerDiameter`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'interno'→'Interno', 'furação'→'Furação', 'olhal'→'Olhal'
- **`ShackleOuterDiameter`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Diâmetro externo do olhal'@pt-br não corresponde ao padrão esperado. Causa: palavra 'externo' deve começar com maiúscula (não é stopword)
- **`ShackleOuterDiameter`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'externo'→'Externo', 'olhal'→'Olhal'
- **`ShackleThickness`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Espessura do olhal'@pt-br não corresponde ao padrão esperado. Causa: palavra 'olhal' deve começar com maiúscula (não é stopword)
- **`ShackleThickness`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'olhal'→'Olhal'
- **`ShearableRiserJoint`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Junta riser cisalhável'@pt-br não corresponde ao padrão esperado. Causa: palavra 'riser' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Shearable riser joint'@en não corresponde ao padrão esperado. Causa: palavra 'riser' deve começar com maiúscula (não é stopword)
- **`ShearableRiserJoint`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'riser'→'Riser', 'joint'→'Joint'; [pt-br] Title Case: 'riser'→'Riser', 'cisalhável'→'Cisalhável'
- **`Socket`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`SolidLayer`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`SolubilityCurveAttribute`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: '(Specific'→'(specific'; [pt-br] Title Case: '(Específica'→'(específica'
- **`SolubilityTable_MoleculeIdentifier`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final; acrônimos em minúsculo: CH4, CO2, H2O, H2S
- **`SolubilityTable_SolubilityCoefficient`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Coeficiente de solubilidade'@pt-br não corresponde ao padrão esperado. Causa: palavra 'solubilidade' deve começar com maiúscula (não é stopword)
- **`SolubilityTable_SolubilityCoefficient`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'solubilidade'→'Solubilidade'
- **`SpecialRequirements`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`SpecificHeatCapacity`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`SpecificWeight`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`SpliceBox`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Caixa de emenda'@pt-br não corresponde ao padrão esperado. Causa: palavra 'emenda' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Splice box'@en não corresponde ao padrão esperado. Causa: palavra 'box' deve começar com maiúscula (não é stopword)
- **`SpliceBox`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'box'→'Box'; [pt-br] Title Case: 'emenda'→'Emenda'
- **`StaticUmbilicalSpan`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`StaticUmbilicalSpan`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Static umbilical span'@en não corresponde ao padrão esperado. Causa: palavra 'umbilical' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Trecho estático de umbilical'@pt-br não corresponde ao padrão esperado. Causa: palavra 'estático' deve começar com maiúscula (não é stopword)
- **`StaticUmbilicalSpan`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'umbilical'→'Umbilical', 'span'→'Span'; [pt-br] Title Case: 'estático'→'Estático', 'umbilical'→'Umbilical'
- **`StiffTorsionalStiffnessAtSeaLevel`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`StiffTorsionalStiffnessAtSeaLevel`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`StorageAccessory`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Acessório de armazenamento/transporte'@pt-br não corresponde ao padrão esperado. Causa: palavra 'armazenamento/transporte' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Storage/transportation accessory'@en não corresponde ao padrão esperado. Causa: palavra 'accessory' deve começar com maiúscula (não é stopword)
- **`StorageAccessory`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'accessory'→'Accessory'; [pt-br] Title Case: 'armazenamento/transporte'→'Armazenamento/transporte'
- **`StorageBox`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Caixa de armazenamento'@pt-br não corresponde ao padrão esperado. Causa: palavra 'armazenamento' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Storage box'@en não corresponde ao padrão esperado. Causa: palavra 'box' deve começar com maiúscula (não é stopword)
- **`StorageBox`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'box'→'Box'; [pt-br] Title Case: 'armazenamento'→'Armazenamento'
- **`StorageSkid`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`StorageSkid`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Skid de armazenamento'@pt-br não corresponde ao padrão esperado. Causa: palavra 'armazenamento' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Storage skid'@en não corresponde ao padrão esperado. Causa: palavra 'skid' deve começar com maiúscula (não é stopword)
- **`StorageSkid`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'skid'→'Skid'; [pt-br] Title Case: 'armazenamento'→'Armazenamento'
- **`StorageSpool`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`StorageSpool`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Carretel de armazenamento'@pt-br não corresponde ao padrão esperado. Causa: palavra 'armazenamento' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Storage spool'@en não corresponde ao padrão esperado. Causa: palavra 'spool' deve começar com maiúscula (não é stopword)
- **`StorageSpool`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'spool'→'Spool'; [pt-br] Title Case: 'armazenamento'→'Armazenamento'
- **`StressAtDesignPressure`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Tensão na pressão de projeto'@pt-br não corresponde ao padrão esperado. Causa: palavra 'pressão' deve começar com maiúscula (não é stopword)
- **`StressAtDesignPressure`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'; [pt-br] Title Case: 'pressão'→'Pressão', 'projeto'→'Projeto'
- **`StrIntOffPLevMaxPress`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`StrIntOffPLevMaxPress`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`StrIntOffPLevMaxPressValRef`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`StrIntOffPLevMaxPressValRef`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`StrIntOffPLevMaxPressValRefMult`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`StrIntOffPLevNomPress`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`StrIntOffPLevNomPress`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`StrIntOffPLevNomPressValRef`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`StrIntOffPLevNomPressValRef`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`StrIntOffPLevNomPressValRefMult`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'At'→'at'
- **`StrIntOnNoTensMaxPress`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`StrIntOnNoTensMaxPress`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'With'→'with'
- **`StrIntOnNoTensMaxPressValRef`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`StrIntOnNoTensMaxPressValRef`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'With'→'with'
- **`StrIntOnNoTensMaxPressValRefMult`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'With'→'with'
- **`StrIntOnNoTensNomPress`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`StrIntOnNoTensNomPress`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'With'→'with'
- **`StrIntOnNoTensNomPressValRef`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`StrIntOnNoTensNomPressValRef`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'With'→'with'
- **`StrIntOnNoTensNomPressValRefMult`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'With'→'with'
- **`Structure`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`StructureApplicationsList`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`StructureCode`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Código da estrutura'@pt-br não corresponde ao padrão esperado. Causa: palavra 'estrutura' deve começar com maiúscula (não é stopword)
- **`StructureCode`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'estrutura'→'Estrutura'
- **`SubProjectId`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Id do Subprojeto'@pt-br não corresponde ao padrão esperado. Causa: acrônimo 'Id' deve ser maiúsculo: ID
  - skos:prefLabel 'Sub Project Id'@en não corresponde ao padrão esperado. Causa: acrônimo 'Id' deve ser maiúsculo: ID
- **`SubProjectId`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] acrônimos: ID; [pt-br] acrônimos: ID
- **`SubseaEquipment`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`SuctionPile`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`SuctionPile`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Estaca de sucção'@pt-br não corresponde ao padrão esperado. Causa: palavra 'sucção' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Suction pile'@en não corresponde ao padrão esperado. Causa: palavra 'pile' deve começar com maiúscula (não é stopword)
- **`SuctionPile`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'pile'→'Pile'; [pt-br] Title Case: 'sucção'→'Sucção'
- **`SupplierProvidedMaterialName`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Nome do material conforme designado pelo fornecedor original do material'@pt-br não corresponde ao padrão esperado. Causa: palavra 'material' deve começar com maiúscula (não é stopword)
- **`SupplierProvidedMaterialName`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'material'→'Material', 'conforme'→'Conforme', 'designado'→'Designado'
- **`SupportRegion`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Região de suporte no Modelo'@pt-br não corresponde ao padrão esperado. Causa: palavra 'suporte' deve começar com maiúscula (não é stopword)
- **`SupportRegion`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'suporte'→'Suporte'
- **`TapesQuantity`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] whitespace extra
- **`TapesQuantity`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Quantidade de fitas'@pt-br não corresponde ao padrão esperado. Causa: palavra 'fitas' deve começar com maiúscula (não é stopword)
- **`TapesQuantity`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'fitas'→'Fitas'
- **`TemperatureSensor`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Sensor de temperatura'@pt-br não corresponde ao padrão esperado. Causa: palavra 'temperatura' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Temperature sensor'@en não corresponde ao padrão esperado. Causa: palavra 'sensor' deve começar com maiúscula (não é stopword)
- **`TemperatureSensor`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'sensor'→'Sensor'; [pt-br] Title Case: 'temperatura'→'Temperatura'
- **`TensileArmourAnnulusCondition`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`TensileArmourFreeAnnulusVolume`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Volume livre do anular das armaduras de tração'@pt-br não corresponde ao padrão esperado. Causa: palavra 'livre' deve começar com maiúscula (não é stopword)
- **`TensileArmourFreeAnnulusVolume`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'livre'→'Livre', 'anular'→'Anular', 'armaduras'→'Armaduras'
- **`TensionerPadsMaterial`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`TensionerPadsShape`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`TensionerTracksQuantity`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`TestBase`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Base de teste'@pt-br não corresponde ao padrão esperado. Causa: palavra 'teste' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Test base'@en não corresponde ao padrão esperado. Causa: palavra 'base' deve começar com maiúscula (não é stopword)
- **`TestBase`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'base'→'Base'; [pt-br] Title Case: 'teste'→'Teste'
- **`TestConditions`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`TestEquipment`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Equipamento de teste'@pt-br não corresponde ao padrão esperado. Causa: palavra 'teste' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Test equipment'@en não corresponde ao padrão esperado. Causa: palavra 'equipment' deve começar com maiúscula (não é stopword)
- **`TestEquipment`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'equipment'→'Equipment'; [pt-br] Title Case: 'teste'→'Teste'
- **`ThermalConductivityCoefficient`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`ThreadsPerInch`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final
- **`ThreadsPerInch`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Per'→'per'
- **`TieIn`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Tie-in'@pt-br não corresponde ao padrão esperado. Causa: palavra 'in' em 'Tie-in' deve começar com maiúscula
- **`TieIn`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Tie-in'→'Tie-In'; [pt-br] Title Case: 'Tie-in'→'Tie-In'
- **`TieInEquipment`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Equipamento de interligação'@pt-br não corresponde ao padrão esperado. Causa: palavra 'interligação' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Tie-in equipment'@en não corresponde ao padrão esperado. Causa: palavra 'equipment' deve começar com maiúscula (não é stopword)
- **`TieInEquipment`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'Tie-in'→'Tie-In', 'equipment'→'Equipment'; [pt-br] Title Case: 'interligação'→'Interligação'
- **`TorpedoPile`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`TorpedoPile`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Estaca-torpedo'@pt-br não corresponde ao padrão esperado. Causa: palavra 'torpedo' em 'Estaca-torpedo' deve começar com maiúscula
  - skos:prefLabel 'Torpedo pile'@en não corresponde ao padrão esperado. Causa: palavra 'pile' deve começar com maiúscula (não é stopword)
- **`TorpedoPile`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'pile'→'Pile'; [pt-br] Title Case: 'Estaca-torpedo'→'Estaca-Torpedo'
- **`TPT`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Pressure and temperature sensor'@en não corresponde ao padrão esperado. Causa: palavra 'temperature' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Sensor de pressão e temperatura'@pt-br não corresponde ao padrão esperado. Causa: palavra 'pressão' deve começar com maiúscula (não é stopword)
- **`TPT`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'temperature'→'Temperature', 'sensor'→'Sensor'; [pt-br] Title Case: 'pressão'→'Pressão', 'temperatura'→'Temperatura'
- **`TransportLineSegment`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`TreeRunningTool`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Ferramenta de instalação de ANM'@pt-br não corresponde ao padrão esperado. Causa: palavra 'instalação' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Wet Christmas tree running tool'@en não corresponde ao padrão esperado. Causa: palavra 'tree' deve começar com maiúscula (não é stopword)
- **`TreeRunningTool`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'tree'→'Tree', 'running'→'Running', 'tool'→'Tool'; [pt-br] Title Case: 'instalação'→'Instalação', 'ANM'→'Anm'
- **`TrianglePlate`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Placa triangular'@pt-br não corresponde ao padrão esperado. Causa: palavra 'triangular' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Triangle plate'@en não corresponde ao padrão esperado. Causa: palavra 'plate' deve começar com maiúscula (não é stopword)
- **`TrianglePlate`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'plate'→'Plate'; [pt-br] Title Case: 'triangular'→'Triangular'
- **`TubingHanger`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`TubingHanger`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Suspensor de coluna'@pt-br não corresponde ao padrão esperado. Causa: palavra 'coluna' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Tubing hanger'@en não corresponde ao padrão esperado. Causa: palavra 'hanger' deve começar com maiúscula (não é stopword)
- **`TubingHanger`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'hanger'→'Hanger'; [pt-br] Title Case: 'coluna'→'Coluna'
- **`TubingHangerRunningTool`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Ferramenta de instalação de TH'@pt-br não corresponde ao padrão esperado. Causa: palavra 'instalação' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Tubing hanger running tool'@en não corresponde ao padrão esperado. Causa: palavra 'hanger' deve começar com maiúscula (não é stopword)
- **`TubingHangerRunningTool`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'hanger'→'Hanger', 'running'→'Running', 'tool'→'Tool'; [pt-br] Title Case: 'instalação'→'Instalação'
- **`TypeLevelAttribute`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`UltimateTensileStress`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`UltTensStrAlongFibers`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Tensão máxima de tração longitudinalmente às fibras'@pt-br não corresponde ao padrão esperado. Causa: palavra 'máxima' deve começar com maiúscula (não é stopword)
- **`UltTensStrAlongFibers`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'máxima'→'Máxima', 'tração'→'Tração', 'longitudinalmente'→'Longitudinalmente'
- **`UltTensStrPerpendFibers`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Tensão máxima de tração perpendicularmente às fibras'@pt-br não corresponde ao padrão esperado. Causa: palavra 'máxima' deve começar com maiúscula (não é stopword)
- **`UltTensStrPerpendFibers`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'To'→'to'; [pt-br] Title Case: 'máxima'→'Máxima', 'tração'→'Tração', 'perpendicularmente'→'Perpendicularmente'
- **`UmbilicalComponent`** — `MULTIPLE_PREFLABEL_SAME_LANG`
  - Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Componente Umbilical', 'Componente de umbilical']
  - Classe tem 2 skos:prefLabel para idioma 'en': ['Umbilical Component', 'Umbilical component']
- **`UmbilicalComponent`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Componente de umbilical'@pt-br não corresponde ao padrão esperado. Causa: palavra 'umbilical' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Umbilical component'@en não corresponde ao padrão esperado. Causa: palavra 'component' deve começar com maiúscula (não é stopword)
- **`UmbilicalComponent`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'component'→'Component'; [pt-br] Title Case: 'umbilical'→'Umbilical'
- **`UmbilicalLocation`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Local de umbilical'@pt-br não corresponde ao padrão esperado. Causa: palavra 'umbilical' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Umbilical location'@en não corresponde ao padrão esperado. Causa: palavra 'location' deve começar com maiúscula (não é stopword)
- **`UmbilicalLocation`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'location'→'Location'; [pt-br] Title Case: 'umbilical'→'Umbilical'
- **`UmbilicalPullingHead`** — `ALTLABEL_TITLECASE_VIOLATION`
  - skos:altLabel 'Cabeça de Manuseio para Umbilical'@pt-br não segue Title Case
- **`UmbilicalSpan`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Trecho de umbilical'@pt-br não corresponde ao padrão esperado. Causa: palavra 'umbilical' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Umbilical span'@en não corresponde ao padrão esperado. Causa: palavra 'span' deve começar com maiúscula (não é stopword)
- **`UmbilicalSpan`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'span'→'Span'; [pt-br] Title Case: 'umbilical'→'Umbilical'
- **`UpperItubeDiameter`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Diâmetro do I-TUBE superior'@pt-br não corresponde ao padrão esperado. Causa: palavra 'superior' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Upper I-tube Diameter'@en não corresponde ao padrão esperado. Causa: acrônimo 'I-tube' deve ser maiúsculo: I-TUBE
- **`UpperItubeDiameter`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] acrônimos: TUBE; [pt-br] Title Case: 'superior'→'Superior'
- **`UTA`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`UTA`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Conjunto de terminação de umbilical'@pt-br não corresponde ao padrão esperado. Causa: palavra 'terminação' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Umbilical termination assembly'@en não corresponde ao padrão esperado. Causa: palavra 'termination' deve começar com maiúscula (não é stopword)
- **`UTA`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'termination'→'Termination', 'assembly'→'Assembly'; [pt-br] Title Case: 'terminação'→'Terminação', 'umbilical'→'Umbilical'
- **`UTM`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Módulo de terminação de umbilical'@pt-br não corresponde ao padrão esperado. Causa: palavra 'terminação' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Umbilical termination module'@en não corresponde ao padrão esperado. Causa: palavra 'termination' deve começar com maiúscula (não é stopword)
- **`UTM`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'termination'→'Termination', 'module'→'Module'; [pt-br] Title Case: 'terminação'→'Terminação', 'umbilical'→'Umbilical'
- **`validValues`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ValueOrigin`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`VCM`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Módulo de conexão vertical'@pt-br não corresponde ao padrão esperado. Causa: palavra 'conexão' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Vertical connection module'@en não corresponde ao padrão esperado. Causa: palavra 'connection' deve começar com maiúscula (não é stopword)
- **`VCM`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'connection'→'Connection', 'module'→'Module'; [pt-br] Title Case: 'conexão'→'Conexão', 'vertical'→'Vertical'
- **`WasteToEnergy`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Energia a partir de Resíduos'@pt-br não corresponde ao padrão esperado. Causa: palavra 'partir' deve começar com maiúscula (não é stopword)
- **`WasteToEnergy`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'partir'→'Partir'
- **`WearBushing`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`WearBushingRunningTool`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Ferramenta de instalação de BD'@pt-br não corresponde ao padrão esperado. Causa: palavra 'instalação' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Wear bushing running tool'@en não corresponde ao padrão esperado. Causa: palavra 'bushing' deve começar com maiúscula (não é stopword)
- **`WearBushingRunningTool`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'bushing'→'Bushing', 'running'→'Running', 'tool'→'Tool'; [pt-br] Title Case: 'instalação'→'Instalação', 'BD'→'Bd'
- **`Wellhead`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Cabeça de poço'@pt-br não corresponde ao padrão esperado. Causa: palavra 'poço' deve começar com maiúscula (não é stopword)
- **`Wellhead`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'poço'→'Poço'
- **`WetChristmasTree`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`WetChristmasTree`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Wet Christmas tree'@en não corresponde ao padrão esperado. Causa: palavra 'tree' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Árvore de Natal molhada'@pt-br não corresponde ao padrão esperado. Causa: palavra 'molhada' deve começar com maiúscula (não é stopword)
- **`WetChristmasTree`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'tree'→'Tree'; [pt-br] Title Case: 'molhada'→'Molhada'
- **`WireRopeQuantity`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [en] falta ponto final
- **`WireRopeQuantity`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Quantidade de cordas de Aço'@pt-br não corresponde ao padrão esperado. Causa: palavra 'cordas' deve começar com maiúscula (não é stopword)
- **`WireRopeQuantity`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'cordas'→'Cordas'
- **`WireRopeSegment`** — `PREFLABEL_FORMAT_INVALID`
  - skos:prefLabel 'Tramo de cabo de aço'@pt-br não corresponde ao padrão esperado. Causa: palavra 'cabo' deve começar com maiúscula (não é stopword)
  - skos:prefLabel 'Wire rope segment'@en não corresponde ao padrão esperado. Causa: palavra 'rope' deve começar com maiúscula (não é stopword)
- **`WireRopeSegment`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: 'rope'→'Rope', 'segment'→'Segment'; [pt-br] Title Case: 'cabo'→'Cabo', 'aço'→'Aço'
- **`WireRopeSlingDiameter`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`WorkingLoadLimit`** — `PREFLABEL_NEEDS_CORRECTION`
  - skos:prefLabel precisa correção. Causa: [en] Title Case: '(WLL)'→'(wll)'
- **`WoundLayer`** — `DEFINITION_NEEDS_CORRECTION`
  - skos:definition precisa correção. Causa: [pt-br] falta ponto final

#### 📖 Legenda dos Códigos

**DomainAttribute:**
| **Código** | **Descrição** |
|------------|---------------|
| `DOMAINATTR_ACCESSRIGHTS_MISSING` | DomainAttribute não possui dcterms:accessRights |
| `DOMAINATTR_IDENTIFIER_MISSING` | DomainAttribute não possui dcterms:identifier |
| `DOMAINATTR_IDENTIFIER_MISMATCH` | dcterms:identifier não corresponde ao local name |
| `DOMAINATTR_DEFINITION_MISSING_EN` | Falta skos:definition em inglês (@en) |
| `DOMAINATTR_DEFINITION_MISSING_PT_BR` | Falta skos:definition em português (@pt-br) |
| `DOMAINATTR_DEFINITION_TOO_MANY_PER_LANG` | Múltiplos skos:definition no mesmo idioma |
| `DOMAINATTR_PREFLABEL_MISSING_EN` | Falta skos:prefLabel em inglês (@en) |
| `DOMAINATTR_PREFLABEL_MISSING_PT_BR` | Falta skos:prefLabel em português (@pt-br) |
| `DOMAINATTR_PREFLABEL_DUPLICATE_PER_LANG` | Múltiplos skos:prefLabel no mesmo idioma |
| `DOMAINATTR_PROPERTY_MISSING` | Propriedade obrigatória ausente (hasAttributeScope, etc.) |

**Classes IFC:**
| **Código** | **Descrição** |
|------------|---------------|
| `IFC_REQUIRED_PROPERTY_MISSING` | Classe IFC sem propriedade obrigatória |
| `IFC_BASE_CLASS_MISSING` | Classe IFC não herda da classe base esperada |

**Geral:**
| **Código** | **Descrição** |
|------------|---------------|
| `CLASS_IDENTIFIER_MISSING` | Classe não possui dcterms:identifier |
| `CLASS_IDENTIFIER_MISMATCH` | dcterms:identifier não corresponde ao local name |
| `MULTIPLE_PREFLABEL_SAME_LANG` | Múltiplos skos:prefLabel no mesmo idioma |
| `MULTIPLE_DEFINITION` | Múltiplos skos:definition no mesmo idioma |
| `ALTLABEL_TITLECASE_VIOLATION` | skos:altLabel não segue Title Case |
| `PREFLABEL_FORMAT_INVALID` | skos:prefLabel não corresponde ao padrão esperado |
| `PREFLABEL_NEEDS_CORRECTION` | skos:prefLabel precisa correção (capitalização, acrônimos) |
| `DEFINITION_NEEDS_CORRECTION` | skos:definition precisa correção (ponto final, acrônimos) |

### 📈 Estatísticas de Erros por Categoria
#### Por Severidade:
- 🟡 **WARNING:** 1207 ocorrências
- 🔴 **ERROR:** 260 ocorrências

#### Top 10 Regras/Códigos Mais Violados:
- `PREFLABEL_FORMAT_INVALID`: 267 ocorrências
- `PREFLABEL_NEEDS_CORRECTION`: 206 ocorrências
- `DOMAINATTR_DEFINITION_MISSING_PT_BR`: 203 ocorrências
- `DEFINITION_NEEDS_CORRECTION`: 195 ocorrências
- `CLASS_IDENTIFIER_MISSING`: 159 ocorrências
- `DOMAINATTR_PROPERTY_MISSING`: 142 ocorrências
- `IFC_REQUIRED_PROPERTY_MISSING`: 62 ocorrências
- `DOMAINATTR_DEFINITION_MISSING_EN`: 33 ocorrências
- `DOMAINATTR_PREFLABEL_MISSING_PT_BR`: 33 ocorrências
- `IFC_BASE_CLASS_MISSING`: 32 ocorrências

---

## 🔍 Detalhamento de Erros

### 📏 Regra: **`ALTLABEL_TITLECASE_VIOLATION`** (12 ocorrências)
- **`FloatingProductionUnit`**
  - Problema: skos:altLabel 'FLNG'@en não segue Title Case
  - Correção: `Flng`
- **`FloatingProductionUnit`**
  - Problema: skos:altLabel 'FPSO'@en não segue Title Case
  - Correção: `Fpso`
- **`FloatingProductionUnit`**
  - Problema: skos:altLabel 'FPU'@en não segue Title Case
  - Correção: `Fpu`
- **`HangOffCollar`**
  - Problema: skos:altLabel 'Hang-Off Clamp'@en não segue Title Case
  - Correção: `Hang-off Clamp`
- **`HangOffCollar`**
  - Problema: skos:altLabel 'Hang-Off Device'@en não segue Title Case
  - Correção: `Hang-off Device`
- **`Jumper`**
  - Problema: skos:altLabel 'Flying lead'@en não segue Title Case
  - Correção: `Flying Lead`
- **`PullInCollar`**
  - Problema: skos:altLabel 'Pull-In Clamp'@en não segue Title Case
  - Correção: `Pull-in Clamp`
- **`RingGasket`**
  - Problema: skos:altLabel ' Seal Ring'@en não segue Title Case
  - Correção: `Seal Ring`
- **`RingGasket`**
  - Problema: skos:altLabel 'O-Ring'@en não segue Title Case
  - Correção: `O-ring`
- **`Shackle`**
  - Problema: skos:altLabel 'D-Shackle'@en não segue Title Case
  - Correção: `D-shackle`
- **`Shackle`**
  - Problema: skos:altLabel 'U-Bolt'@en não segue Title Case
  - Correção: `U-bolt`
- **`UmbilicalPullingHead`**
  - Problema: skos:altLabel 'Cabeça de Manuseio para Umbilical'@pt-br não segue Title Case
  - Correção: `Cabeça De Manuseio Para Umbilical`

### 📏 Regra: **`CLASS_IDENTIFIER_MISMATCH`** (7 ocorrências)
- **`BendMomentVsShearForceTableColumn`**
  - Problema: dcterms:identifier 'BendMomentVsShearForceTable' não corresponde ao local name 'BendMomentVsShearForceTableColumn'
  - Correção: `BendMomentVsShearForceTableColumn`
- **`CommissioningElement`**
  - Problema: dcterms:identifier 'CommissioningObject' não corresponde ao local name 'CommissioningElement'
  - Correção: `CommissioningElement`
- **`DiffusionTableColumn`**
  - Problema: dcterms:identifier 'DiffusionTable' não corresponde ao local name 'DiffusionTableColumn'
  - Correção: `DiffusionTableColumn`
- **`InternalIncidentalPressureCurveAttribute`**
  - Problema: dcterms:identifier 'InternalIncidentalPressureTable' não corresponde ao local name 'InternalIncidentalPressureCurveAttribute'
  - Correção: `InternalIncidentalPressureCurveAttribute`
- **`MaxDesignAbsIntPresCurveAttribute`**
  - Problema: dcterms:identifier 'MaxDesignAbsIntPresTable' não corresponde ao local name 'MaxDesignAbsIntPresCurveAttribute'
  - Correção: `MaxDesignAbsIntPresCurveAttribute`
- **`PermeabilityCurveAttribute`**
  - Problema: dcterms:identifier 'PermeabilityTable' não corresponde ao local name 'PermeabilityCurveAttribute'
  - Correção: `PermeabilityCurveAttribute`
- **`SolubilityCurveAttribute`**
  - Problema: dcterms:identifier 'SolubilityTable' não corresponde ao local name 'SolubilityCurveAttribute'
  - Correção: `SolubilityCurveAttribute`

### 📏 Regra: **`CLASS_IDENTIFIER_MISSING`** (159 ocorrências)
*Mostrando 20 de 159 exemplos*
- **`AdministrativeAttribute`**
  - Problema: Classe 'AdministrativeAttribute' não possui dcterms:identifier
  - Correção: `AdministrativeAttribute`
- **`AnyURIType`**
  - Problema: Classe 'AnyURIType' não possui dcterms:identifier
  - Correção: `AnyURIType`
- **`ArchitecturalEngineering`**
  - Problema: Classe 'ArchitecturalEngineering' não possui dcterms:identifier
  - Correção: `ArchitecturalEngineering`
- **`AttributeClassification`**
  - Problema: Classe 'AttributeClassification' não possui dcterms:identifier
  - Correção: `AttributeClassification`
- **`AttributeDomainCategory`**
  - Problema: Classe 'AttributeDomainCategory' não possui dcterms:identifier
  - Correção: `AttributeDomainCategory`
- **`AttributeNature`**
  - Problema: Classe 'AttributeNature' não possui dcterms:identifier
  - Correção: `AttributeNature`
- **`AttributeScope`**
  - Problema: Classe 'AttributeScope' não possui dcterms:identifier
  - Correção: `AttributeScope`
- **`AttributeValueCardinality`**
  - Problema: Classe 'AttributeValueCardinality' não possui dcterms:identifier
  - Correção: `AttributeValueCardinality`
- **`AttributesGroup`**
  - Problema: Classe 'AttributesGroup' não possui dcterms:identifier
  - Correção: `AttributesGroup`
- **`AutomationControlEngineering`**
  - Problema: Classe 'AutomationControlEngineering' não possui dcterms:identifier
  - Correção: `AutomationControlEngineering`
- **`Base64BinaryType`**
  - Problema: Classe 'Base64BinaryType' não possui dcterms:identifier
  - Correção: `Base64BinaryType`
- **`BasicDesign`**
  - Problema: Classe 'BasicDesign' não possui dcterms:identifier
  - Correção: `BasicDesign`
- **`BatchLevelAttribute`**
  - Problema: Classe 'BatchLevelAttribute' não possui dcterms:identifier
  - Correção: `BatchLevelAttribute`
- **`BendMomentVsShearForceCurveAttribute`**
  - Problema: Classe 'BendMomentVsShearForceCurveAttribute' não possui dcterms:identifier
  - Correção: `BendMomentVsShearForceCurveAttribute`
- **`BendingStiffnessCurveAttribute`**
  - Problema: Classe 'BendingStiffnessCurveAttribute' não possui dcterms:identifier
  - Correção: `BendingStiffnessCurveAttribute`
- **`BendingStiffnessTableColumn`**
  - Problema: Classe 'BendingStiffnessTableColumn' não possui dcterms:identifier
  - Correção: `BendingStiffnessTableColumn`
- **`Biomass`**
  - Problema: Classe 'Biomass' não possui dcterms:identifier
  - Correção: `Biomass`
- **`BooleanValue`**
  - Problema: Classe 'BooleanValue' não possui dcterms:identifier
  - Correção: `BooleanValue`
- **`CalculatedValue`**
  - Problema: Classe 'CalculatedValue' não possui dcterms:identifier
  - Correção: `CalculatedValue`
- **`CivilEngineering`**
  - Problema: Classe 'CivilEngineering' não possui dcterms:identifier
  - Correção: `CivilEngineering`

### 📏 Regra: **`DEFINITION_NEEDS_CORRECTION`** (195 ocorrências)
*Mostrando 20 de 195 exemplos*
- **`hasAttributeGroup`**
  - Problema: skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`AttributeDomainCategory`**
  - Problema: skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`Hub`**
  - Problema: skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`FlowlineSpan`**
  - Problema: skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`HydrostaticCollapseAbsPressDry`**
  - Problema: skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`StrIntOffPLevNomPress`**
  - Problema: skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`ChokeModule`**
  - Problema: skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`hasLifecycleCreationPhase`**
  - Problema: skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`MetallicStrandLength`**
  - Problema: skos:definition precisa correção. Causa: [en] falta ponto final
- **`ConnectionModule`**
  - Problema: skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`ValueOrigin`**
  - Problema: skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`DiffusionTable_MoleculeIdentifier`**
  - Problema: skos:definition precisa correção. Causa: [pt-br] falta ponto final; acrônimos em minúsculo: CH4, CO2, H2O, H2S
- **`UltimateTensileStress`**
  - Problema: skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`HubProtectionCap`**
  - Problema: skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`hasValueCardinality`**
  - Problema: skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`CalculatedValue`**
  - Problema: skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`MasterControlStation`**
  - Problema: skos:definition precisa correção. Causa: [en] falta ponto final; [pt-br] falta ponto final
- **`GroovePoint`**
  - Problema: skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`StrIntOnNoTensNomPressValRef`**
  - Problema: skos:definition precisa correção. Causa: [pt-br] falta ponto final
- **`WoundLayer`**
  - Problema: skos:definition precisa correção. Causa: [pt-br] falta ponto final

### 📏 Regra: **`DOMAINATTR_ACCESSRIGHTS_MISSING`** (31 ocorrências)
*Mostrando 20 de 31 exemplos*
- **`BendMomentVsShearForceCurveAttribute`**
  - Problema: DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui dcterms:accessRights
- **`BendingStiffnessCurveAttribute`**
  - Problema: DomainAttribute 'BendingStiffnessCurveAttribute' não possui dcterms:accessRights
- **`BendingStiffnessTableColumn`**
  - Problema: DomainAttribute 'BendingStiffnessTableColumn' não possui dcterms:accessRights
- **`CrushingCurveAttribute`**
  - Problema: DomainAttribute 'CrushingCurveAttribute' não possui dcterms:accessRights
- **`CrushingFrictionCoefficientTighteningAttribute`**
  - Problema: DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui dcterms:accessRights
- **`CrushingFrictionCoefficientTighteningTableColumn`**
  - Problema: DomainAttribute 'CrushingFrictionCoefficientTighteningTableColumn' não possui dcterms:accessRights
- **`CrushingMaximumAllowableTensionAttribute`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTensionAttribute' não possui dcterms:accessRights
- **`CrushingMaximumAllowableTensionTableColumn`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTensionTableColumn' não possui dcterms:accessRights
- **`CrushingMaximumAllowableTighteningAttribute`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTighteningAttribute' não possui dcterms:accessRights
- **`CrushingMaximumAllowableTighteningTableColumn`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTighteningTableColumn' não possui dcterms:accessRights
- **`DiffusionCurveAttribute`**
  - Problema: DomainAttribute 'DiffusionCurveAttribute' não possui dcterms:accessRights
- **`DimensionsTableColumn`**
  - Problema: DomainAttribute 'DimensionsTableColumn' não possui dcterms:accessRights
- **`DrawingDimensionsTableAttribute`**
  - Problema: DomainAttribute 'DrawingDimensionsTableAttribute' não possui dcterms:accessRights
- **`EModVsTempCurveAttribute`**
  - Problema: DomainAttribute 'EModVsTempCurveAttribute' não possui dcterms:accessRights
- **`EModVsTempTableColumn`**
  - Problema: DomainAttribute 'EModVsTempTableColumn' não possui dcterms:accessRights
- **`EarlyLeakMaxPressTableAttribute`**
  - Problema: DomainAttribute 'EarlyLeakMaxPressTableAttribute' não possui dcterms:accessRights
- **`EarlyLeakMaxPressTableColumn`**
  - Problema: DomainAttribute 'EarlyLeakMaxPressTableColumn' não possui dcterms:accessRights
- **`EarlyLeakNomPressTableAttribute`**
  - Problema: DomainAttribute 'EarlyLeakNomPressTableAttribute' não possui dcterms:accessRights
- **`EarlyLeakNomPressTableColumn`**
  - Problema: DomainAttribute 'EarlyLeakNomPressTableColumn' não possui dcterms:accessRights
- **`FlangeAttribute`**
  - Problema: DomainAttribute 'FlangeAttribute' não possui dcterms:accessRights

### 📏 Regra: **`DOMAINATTR_DEFINITION_MISSING_EN`** (33 ocorrências)
*Mostrando 20 de 33 exemplos*
- **`BendMomentVsShearForceCurveAttribute`**
  - Problema: DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui skos:definition em inglês (@en)
- **`BendingStiffnessCurveAttribute`**
  - Problema: DomainAttribute 'BendingStiffnessCurveAttribute' não possui skos:definition em inglês (@en)
- **`BendingStiffnessTableColumn`**
  - Problema: DomainAttribute 'BendingStiffnessTableColumn' não possui skos:definition em inglês (@en)
- **`CrushingCurveAttribute`**
  - Problema: DomainAttribute 'CrushingCurveAttribute' não possui skos:definition em inglês (@en)
- **`CrushingFrictionCoefficientTighteningAttribute`**
  - Problema: DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui skos:definition em inglês (@en)
- **`CrushingFrictionCoefficientTighteningTableColumn`**
  - Problema: DomainAttribute 'CrushingFrictionCoefficientTighteningTableColumn' não possui skos:definition em inglês (@en)
- **`CrushingMaximumAllowableTensionAttribute`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTensionAttribute' não possui skos:definition em inglês (@en)
- **`CrushingMaximumAllowableTensionTableColumn`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTensionTableColumn' não possui skos:definition em inglês (@en)
- **`CrushingMaximumAllowableTighteningAttribute`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTighteningAttribute' não possui skos:definition em inglês (@en)
- **`CrushingMaximumAllowableTighteningTableColumn`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTighteningTableColumn' não possui skos:definition em inglês (@en)
- **`DiffusionCurveAttribute`**
  - Problema: DomainAttribute 'DiffusionCurveAttribute' não possui skos:definition em inglês (@en)
- **`DimensionsTableColumn`**
  - Problema: DomainAttribute 'DimensionsTableColumn' não possui skos:definition em inglês (@en)
- **`DrawingDimensionsTableAttribute`**
  - Problema: DomainAttribute 'DrawingDimensionsTableAttribute' não possui skos:definition em inglês (@en)
- **`EModVsTempCurveAttribute`**
  - Problema: DomainAttribute 'EModVsTempCurveAttribute' não possui skos:definition em inglês (@en)
- **`EModVsTempTableColumn`**
  - Problema: DomainAttribute 'EModVsTempTableColumn' não possui skos:definition em inglês (@en)
- **`EarlyLeakMaxPressTableAttribute`**
  - Problema: DomainAttribute 'EarlyLeakMaxPressTableAttribute' não possui skos:definition em inglês (@en)
- **`EarlyLeakMaxPressTableColumn`**
  - Problema: DomainAttribute 'EarlyLeakMaxPressTableColumn' não possui skos:definition em inglês (@en)
- **`EarlyLeakNomPressTableAttribute`**
  - Problema: DomainAttribute 'EarlyLeakNomPressTableAttribute' não possui skos:definition em inglês (@en)
- **`EarlyLeakNomPressTableColumn`**
  - Problema: DomainAttribute 'EarlyLeakNomPressTableColumn' não possui skos:definition em inglês (@en)
- **`FlangeAttribute`**
  - Problema: DomainAttribute 'FlangeAttribute' não possui skos:definition em inglês (@en)

### 📏 Regra: **`DOMAINATTR_DEFINITION_MISSING_PT_BR`** (203 ocorrências)
*Mostrando 20 de 203 exemplos*
- **`AbsoluteInsidePressure`**
  - Problema: DomainAttribute 'AbsoluteInsidePressure' não possui skos:definition em português (@pt-br)
- **`AbsoluteOutsidePressure`**
  - Problema: DomainAttribute 'AbsoluteOutsidePressure' não possui skos:definition em português (@pt-br)
- **`AnodeCollarsAxialSpacing`**
  - Problema: DomainAttribute 'AnodeCollarsAxialSpacing' não possui skos:definition em português (@pt-br)
- **`AnodeCollarsQuantity`**
  - Problema: DomainAttribute 'AnodeCollarsQuantity' não possui skos:definition em português (@pt-br)
- **`AssemblyShouldObeyModelPolarity`**
  - Problema: DomainAttribute 'AssemblyShouldObeyModelPolarity' não possui skos:definition em português (@pt-br)
- **`AssemblyTorque`**
  - Problema: DomainAttribute 'AssemblyTorque' não possui skos:definition em português (@pt-br)
- **`BendMomentVsShearForceCurveAttribute`**
  - Problema: DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui skos:definition em português (@pt-br)
- **`BendMomentVsShearForceTableColumn`**
  - Problema: DomainAttribute 'BendMomentVsShearForceTableColumn' não possui skos:definition em português (@pt-br)
- **`BendMomentVsShearForceTable_BendingMoment`**
  - Problema: DomainAttribute 'BendMomentVsShearForceTable_BendingMoment' não possui skos:definition em português (@pt-br)
- **`BendMomentVsShearForceTable_Condition`**
  - Problema: DomainAttribute 'BendMomentVsShearForceTable_Condition' não possui skos:definition em português (@pt-br)
- **`BendingMomentTable_BendingMoment`**
  - Problema: DomainAttribute 'BendingMomentTable_BendingMoment' não possui skos:definition em português (@pt-br)
- **`BendingMomentTable_Curvature`**
  - Problema: DomainAttribute 'BendingMomentTable_Curvature' não possui skos:definition em português (@pt-br)
- **`BendingStiffnessCurveAttribute`**
  - Problema: DomainAttribute 'BendingStiffnessCurveAttribute' não possui skos:definition em português (@pt-br)
- **`BendingStiffnessTableColumn`**
  - Problema: DomainAttribute 'BendingStiffnessTableColumn' não possui skos:definition em português (@pt-br)
- **`BoreDiameter`**
  - Problema: DomainAttribute 'BoreDiameter' não possui skos:definition em português (@pt-br)
- **`CO2VolumePercentage`**
  - Problema: DomainAttribute 'CO2VolumePercentage' não possui skos:definition em português (@pt-br)
- **`CalculatedAbsoluteBurstPressure`**
  - Problema: DomainAttribute 'CalculatedAbsoluteBurstPressure' não possui skos:definition em português (@pt-br)
- **`ClampInternalDiameter`**
  - Problema: DomainAttribute 'ClampInternalDiameter' não possui skos:definition em português (@pt-br)
- **`CollarInternalDiameter`**
  - Problema: DomainAttribute 'CollarInternalDiameter' não possui skos:definition em português (@pt-br)
- **`CompositeLayerMaterialType`**
  - Problema: DomainAttribute 'CompositeLayerMaterialType' não possui skos:definition em português (@pt-br)

### 📏 Regra: **`DOMAINATTR_IDENTIFIER_MISMATCH`** (6 ocorrências)
- **`BendMomentVsShearForceTableColumn`**
  - Problema: dcterms:identifier 'BendMomentVsShearForceTable' não corresponde ao local name 'BendMomentVsShearForceTableColumn'
  - Correção: `BendMomentVsShearForceTableColumn`
- **`DiffusionTableColumn`**
  - Problema: dcterms:identifier 'DiffusionTable' não corresponde ao local name 'DiffusionTableColumn'
  - Correção: `DiffusionTableColumn`
- **`InternalIncidentalPressureCurveAttribute`**
  - Problema: dcterms:identifier 'InternalIncidentalPressureTable' não corresponde ao local name 'InternalIncidentalPressureCurveAttribute'
  - Correção: `InternalIncidentalPressureCurveAttribute`
- **`MaxDesignAbsIntPresCurveAttribute`**
  - Problema: dcterms:identifier 'MaxDesignAbsIntPresTable' não corresponde ao local name 'MaxDesignAbsIntPresCurveAttribute'
  - Correção: `MaxDesignAbsIntPresCurveAttribute`
- **`PermeabilityCurveAttribute`**
  - Problema: dcterms:identifier 'PermeabilityTable' não corresponde ao local name 'PermeabilityCurveAttribute'
  - Correção: `PermeabilityCurveAttribute`
- **`SolubilityCurveAttribute`**
  - Problema: dcterms:identifier 'SolubilityTable' não corresponde ao local name 'SolubilityCurveAttribute'
  - Correção: `SolubilityCurveAttribute`

### 📏 Regra: **`DOMAINATTR_IDENTIFIER_MISSING`** (31 ocorrências)
*Mostrando 20 de 31 exemplos*
- **`BendMomentVsShearForceCurveAttribute`**
  - Problema: DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui dcterms:identifier
  - Correção: `BendMomentVsShearForceCurveAttribute`
- **`BendingStiffnessCurveAttribute`**
  - Problema: DomainAttribute 'BendingStiffnessCurveAttribute' não possui dcterms:identifier
  - Correção: `BendingStiffnessCurveAttribute`
- **`BendingStiffnessTableColumn`**
  - Problema: DomainAttribute 'BendingStiffnessTableColumn' não possui dcterms:identifier
  - Correção: `BendingStiffnessTableColumn`
- **`CrushingCurveAttribute`**
  - Problema: DomainAttribute 'CrushingCurveAttribute' não possui dcterms:identifier
  - Correção: `CrushingCurveAttribute`
- **`CrushingFrictionCoefficientTighteningAttribute`**
  - Problema: DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui dcterms:identifier
  - Correção: `CrushingFrictionCoefficientTighteningAttribute`
- **`CrushingFrictionCoefficientTighteningTableColumn`**
  - Problema: DomainAttribute 'CrushingFrictionCoefficientTighteningTableColumn' não possui dcterms:identifier
  - Correção: `CrushingFrictionCoefficientTighteningTableColumn`
- **`CrushingMaximumAllowableTensionAttribute`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTensionAttribute' não possui dcterms:identifier
  - Correção: `CrushingMaximumAllowableTensionAttribute`
- **`CrushingMaximumAllowableTensionTableColumn`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTensionTableColumn' não possui dcterms:identifier
  - Correção: `CrushingMaximumAllowableTensionTableColumn`
- **`CrushingMaximumAllowableTighteningAttribute`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTighteningAttribute' não possui dcterms:identifier
  - Correção: `CrushingMaximumAllowableTighteningAttribute`
- **`CrushingMaximumAllowableTighteningTableColumn`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTighteningTableColumn' não possui dcterms:identifier
  - Correção: `CrushingMaximumAllowableTighteningTableColumn`
- **`DiffusionCurveAttribute`**
  - Problema: DomainAttribute 'DiffusionCurveAttribute' não possui dcterms:identifier
  - Correção: `DiffusionCurveAttribute`
- **`DimensionsTableColumn`**
  - Problema: DomainAttribute 'DimensionsTableColumn' não possui dcterms:identifier
  - Correção: `DimensionsTableColumn`
- **`DrawingDimensionsTableAttribute`**
  - Problema: DomainAttribute 'DrawingDimensionsTableAttribute' não possui dcterms:identifier
  - Correção: `DrawingDimensionsTableAttribute`
- **`EModVsTempCurveAttribute`**
  - Problema: DomainAttribute 'EModVsTempCurveAttribute' não possui dcterms:identifier
  - Correção: `EModVsTempCurveAttribute`
- **`EModVsTempTableColumn`**
  - Problema: DomainAttribute 'EModVsTempTableColumn' não possui dcterms:identifier
  - Correção: `EModVsTempTableColumn`
- **`EarlyLeakMaxPressTableAttribute`**
  - Problema: DomainAttribute 'EarlyLeakMaxPressTableAttribute' não possui dcterms:identifier
  - Correção: `EarlyLeakMaxPressTableAttribute`
- **`EarlyLeakMaxPressTableColumn`**
  - Problema: DomainAttribute 'EarlyLeakMaxPressTableColumn' não possui dcterms:identifier
  - Correção: `EarlyLeakMaxPressTableColumn`
- **`EarlyLeakNomPressTableAttribute`**
  - Problema: DomainAttribute 'EarlyLeakNomPressTableAttribute' não possui dcterms:identifier
  - Correção: `EarlyLeakNomPressTableAttribute`
- **`EarlyLeakNomPressTableColumn`**
  - Problema: DomainAttribute 'EarlyLeakNomPressTableColumn' não possui dcterms:identifier
  - Correção: `EarlyLeakNomPressTableColumn`
- **`FlangeAttribute`**
  - Problema: DomainAttribute 'FlangeAttribute' não possui dcterms:identifier
  - Correção: `FlangeAttribute`

### 📏 Regra: **`DOMAINATTR_PREFLABEL_MISSING_EN`** (31 ocorrências)
*Mostrando 20 de 31 exemplos*
- **`BendMomentVsShearForceCurveAttribute`**
  - Problema: DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui skos:prefLabel em inglês (@en)
- **`BendingStiffnessCurveAttribute`**
  - Problema: DomainAttribute 'BendingStiffnessCurveAttribute' não possui skos:prefLabel em inglês (@en)
- **`BendingStiffnessTableColumn`**
  - Problema: DomainAttribute 'BendingStiffnessTableColumn' não possui skos:prefLabel em inglês (@en)
- **`CrushingCurveAttribute`**
  - Problema: DomainAttribute 'CrushingCurveAttribute' não possui skos:prefLabel em inglês (@en)
- **`CrushingFrictionCoefficientTighteningAttribute`**
  - Problema: DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui skos:prefLabel em inglês (@en)
- **`CrushingFrictionCoefficientTighteningTableColumn`**
  - Problema: DomainAttribute 'CrushingFrictionCoefficientTighteningTableColumn' não possui skos:prefLabel em inglês (@en)
- **`CrushingMaximumAllowableTensionAttribute`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTensionAttribute' não possui skos:prefLabel em inglês (@en)
- **`CrushingMaximumAllowableTensionTableColumn`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTensionTableColumn' não possui skos:prefLabel em inglês (@en)
- **`CrushingMaximumAllowableTighteningAttribute`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTighteningAttribute' não possui skos:prefLabel em inglês (@en)
- **`CrushingMaximumAllowableTighteningTableColumn`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTighteningTableColumn' não possui skos:prefLabel em inglês (@en)
- **`DiffusionCurveAttribute`**
  - Problema: DomainAttribute 'DiffusionCurveAttribute' não possui skos:prefLabel em inglês (@en)
- **`DimensionsTableColumn`**
  - Problema: DomainAttribute 'DimensionsTableColumn' não possui skos:prefLabel em inglês (@en)
- **`DrawingDimensionsTableAttribute`**
  - Problema: DomainAttribute 'DrawingDimensionsTableAttribute' não possui skos:prefLabel em inglês (@en)
- **`EModVsTempCurveAttribute`**
  - Problema: DomainAttribute 'EModVsTempCurveAttribute' não possui skos:prefLabel em inglês (@en)
- **`EModVsTempTableColumn`**
  - Problema: DomainAttribute 'EModVsTempTableColumn' não possui skos:prefLabel em inglês (@en)
- **`EarlyLeakMaxPressTableAttribute`**
  - Problema: DomainAttribute 'EarlyLeakMaxPressTableAttribute' não possui skos:prefLabel em inglês (@en)
- **`EarlyLeakMaxPressTableColumn`**
  - Problema: DomainAttribute 'EarlyLeakMaxPressTableColumn' não possui skos:prefLabel em inglês (@en)
- **`EarlyLeakNomPressTableAttribute`**
  - Problema: DomainAttribute 'EarlyLeakNomPressTableAttribute' não possui skos:prefLabel em inglês (@en)
- **`EarlyLeakNomPressTableColumn`**
  - Problema: DomainAttribute 'EarlyLeakNomPressTableColumn' não possui skos:prefLabel em inglês (@en)
- **`FlangeAttribute`**
  - Problema: DomainAttribute 'FlangeAttribute' não possui skos:prefLabel em inglês (@en)

### 📏 Regra: **`DOMAINATTR_PREFLABEL_MISSING_PT_BR`** (33 ocorrências)
*Mostrando 20 de 33 exemplos*
- **`BendMomentVsShearForceCurveAttribute`**
  - Problema: DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui skos:prefLabel em português (@pt-br)
- **`BendingStiffnessCurveAttribute`**
  - Problema: DomainAttribute 'BendingStiffnessCurveAttribute' não possui skos:prefLabel em português (@pt-br)
- **`BendingStiffnessTableColumn`**
  - Problema: DomainAttribute 'BendingStiffnessTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`CrushingCurveAttribute`**
  - Problema: DomainAttribute 'CrushingCurveAttribute' não possui skos:prefLabel em português (@pt-br)
- **`CrushingFrictionCoefficientTighteningAttribute`**
  - Problema: DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui skos:prefLabel em português (@pt-br)
- **`CrushingFrictionCoefficientTighteningTableColumn`**
  - Problema: DomainAttribute 'CrushingFrictionCoefficientTighteningTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`CrushingMaximumAllowableTensionAttribute`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTensionAttribute' não possui skos:prefLabel em português (@pt-br)
- **`CrushingMaximumAllowableTensionTableColumn`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTensionTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`CrushingMaximumAllowableTighteningAttribute`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTighteningAttribute' não possui skos:prefLabel em português (@pt-br)
- **`CrushingMaximumAllowableTighteningTableColumn`**
  - Problema: DomainAttribute 'CrushingMaximumAllowableTighteningTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`DiffusionCurveAttribute`**
  - Problema: DomainAttribute 'DiffusionCurveAttribute' não possui skos:prefLabel em português (@pt-br)
- **`DimensionsTableColumn`**
  - Problema: DomainAttribute 'DimensionsTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`DrawingDimensionsTableAttribute`**
  - Problema: DomainAttribute 'DrawingDimensionsTableAttribute' não possui skos:prefLabel em português (@pt-br)
- **`EModVsTempCurveAttribute`**
  - Problema: DomainAttribute 'EModVsTempCurveAttribute' não possui skos:prefLabel em português (@pt-br)
- **`EModVsTempTableColumn`**
  - Problema: DomainAttribute 'EModVsTempTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`EModVsTempTable_Temperature`**
  - Problema: DomainAttribute 'EModVsTempTable_Temperature' não possui skos:prefLabel em português (@pt-br)
- **`EarlyLeakMaxPressTableAttribute`**
  - Problema: DomainAttribute 'EarlyLeakMaxPressTableAttribute' não possui skos:prefLabel em português (@pt-br)
- **`EarlyLeakMaxPressTableColumn`**
  - Problema: DomainAttribute 'EarlyLeakMaxPressTableColumn' não possui skos:prefLabel em português (@pt-br)
- **`EarlyLeakNomPressTableAttribute`**
  - Problema: DomainAttribute 'EarlyLeakNomPressTableAttribute' não possui skos:prefLabel em português (@pt-br)
- **`EarlyLeakNomPressTableColumn`**
  - Problema: DomainAttribute 'EarlyLeakNomPressTableColumn' não possui skos:prefLabel em português (@pt-br)

### 📏 Regra: **`DOMAINATTR_PROPERTY_MISSING`** (142 ocorrências)
*Mostrando 20 de 142 exemplos*
- **`BendMomentVsShearForceCurveAttribute`**
  - Problema: DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
- **`BendMomentVsShearForceCurveAttribute`**
  - Problema: DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
- **`BendMomentVsShearForceCurveAttribute`**
  - Problema: DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui propriedade obrigatória: edo:hasTypedValue
- **`BendMomentVsShearForceCurveAttribute`**
  - Problema: DomainAttribute 'BendMomentVsShearForceCurveAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`BendMomentVsShearForceTableColumn`**
  - Problema: DomainAttribute 'BendMomentVsShearForceTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
- **`BendMomentVsShearForceTableColumn`**
  - Problema: DomainAttribute 'BendMomentVsShearForceTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
- **`BendMomentVsShearForceTableColumn`**
  - Problema: DomainAttribute 'BendMomentVsShearForceTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`BendingStiffnessCurveAttribute`**
  - Problema: DomainAttribute 'BendingStiffnessCurveAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
- **`BendingStiffnessCurveAttribute`**
  - Problema: DomainAttribute 'BendingStiffnessCurveAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
- **`BendingStiffnessCurveAttribute`**
  - Problema: DomainAttribute 'BendingStiffnessCurveAttribute' não possui propriedade obrigatória: edo:hasTypedValue
- **`BendingStiffnessCurveAttribute`**
  - Problema: DomainAttribute 'BendingStiffnessCurveAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`BendingStiffnessTableColumn`**
  - Problema: DomainAttribute 'BendingStiffnessTableColumn' não possui propriedade obrigatória: edo:hasAttributeScope
- **`BendingStiffnessTableColumn`**
  - Problema: DomainAttribute 'BendingStiffnessTableColumn' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
- **`BendingStiffnessTableColumn`**
  - Problema: DomainAttribute 'BendingStiffnessTableColumn' não possui propriedade obrigatória: edo:hasTypedValue
- **`BendingStiffnessTableColumn`**
  - Problema: DomainAttribute 'BendingStiffnessTableColumn' não possui propriedade obrigatória: edo:hasValueCardinality
- **`CrushingCurveAttribute`**
  - Problema: DomainAttribute 'CrushingCurveAttribute' não possui propriedade obrigatória: edo:hasAttributeScope
- **`CrushingCurveAttribute`**
  - Problema: DomainAttribute 'CrushingCurveAttribute' não possui propriedade obrigatória: edo:hasLifecycleCreationPhase
- **`CrushingCurveAttribute`**
  - Problema: DomainAttribute 'CrushingCurveAttribute' não possui propriedade obrigatória: edo:hasTypedValue
- **`CrushingCurveAttribute`**
  - Problema: DomainAttribute 'CrushingCurveAttribute' não possui propriedade obrigatória: edo:hasValueCardinality
- **`CrushingFrictionCoefficientTighteningAttribute`**
  - Problema: DomainAttribute 'CrushingFrictionCoefficientTighteningAttribute' não possui propriedade obrigatória: edo:hasAttributeScope

### 📏 Regra: **`IFC_BASE_CLASS_MISSING`** (32 ocorrências)
*Mostrando 20 de 32 exemplos*
- **`AbandonmentCap`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`AbrasionProtector`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningActivity`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningContract`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningDigitalProcessStep`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningEvidence`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningIssue`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningItemCheck`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningLoopCheck`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningPerson`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningPreservationOrder`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningProgram`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningProject`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningResponsibleActor`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningResponsibleGroup`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`CommissioningTask`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`ElectricalJumperConnector`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`ElectricalPowerJumperConnector`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`FlangeAdapter`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement
- **`FlangeConnection`**
  - Problema: Classe IFC não herda de edo:IfcInstanciableElement

### 📏 Regra: **`IFC_REQUIRED_PROPERTY_MISSING`** (62 ocorrências)
*Mostrando 20 de 62 exemplos*
- **`AbandonmentCap`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`AbrasionProtector`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`BendRestrictor`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`CommissioningActivity`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningContract`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningDigitalProcessStep`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningEvidence`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningIssue`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningItemCheck`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningLoopCheck`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningPerson`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningPreservationOrder`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningProgram`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningProject`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningResponsibleActor`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningResponsibleGroup`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CommissioningTask`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:hasDiscipline
- **`CompositeMaterial`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`DimensionsDrawing`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:ifc_predefinedType
- **`DynamicUmbilicalSpan`**
  - Problema: Classe IFC sem propriedade obrigatória: edo:ifc_equivalentClass

### 📏 Regra: **`MULTIPLE_DEFINITION`** (3 ocorrências)
- **`HCRHose`**
  - Problema: Classe tem 2 skos:definition para idioma 'en' (máximo: 1)
- **`LogicalElement`**
  - Problema: Classe tem 2 skos:definition para idioma 'pt-br' (máximo: 1)
- **`LogicalElement`**
  - Problema: Classe tem 2 skos:definition para idioma 'en' (máximo: 1)

### 📏 Regra: **`MULTIPLE_PREFLABEL_SAME_LANG`** (14 ocorrências)
- **`ElectricalCable`**
  - Problema: Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Cabo Elétrico', 'Cabo elétrico']
- **`ElectricalCable`**
  - Problema: Classe tem 2 skos:prefLabel para idioma 'en': ['Electrical Cable', 'Electrical cable']
- **`Filler`**
  - Problema: Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Enchimento', 'Preenchimento']
- **`FunctionLine`**
  - Problema: Classe tem 2 skos:prefLabel para idioma 'en': ['Function Line', 'Function line']
- **`FunctionLine`**
  - Problema: Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Linha Funcional', 'Linha de função']
- **`IntegratedPipe`**
  - Problema: Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Duto integrado', 'Tubo Integrado']
- **`IntegratedPipe`**
  - Problema: Classe tem 2 skos:prefLabel para idioma 'en': ['Integrated Pipe', 'Integrated pipe']
- **`MetallicTubing`**
  - Problema: Classe tem 2 skos:prefLabel para idioma 'en': ['Metallic Tubing', 'Metallic tubing']
- **`MetallicTubing`**
  - Problema: Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Tubulação Metálica', 'Tubulação metálica']
- **`OpticalFiberCable`**
  - Problema: Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Cabo de Fibra Óptica', 'Cabo de fibra ótica']
- **`OpticalFiberCable`**
  - Problema: Classe tem 2 skos:prefLabel para idioma 'en': ['Optical Fiber Cable', 'Optical fiber cable']
- **`PlasticHose`**
  - Problema: Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Mangueira Plástica', 'Mangueira plástica']
- **`UmbilicalComponent`**
  - Problema: Classe tem 2 skos:prefLabel para idioma 'pt-br': ['Componente Umbilical', 'Componente de umbilical']
- **`UmbilicalComponent`**
  - Problema: Classe tem 2 skos:prefLabel para idioma 'en': ['Umbilical Component', 'Umbilical component']

### 📏 Regra: **`PREFLABEL_FORMAT_INVALID`** (267 ocorrências)
*Mostrando 20 de 267 exemplos*
- **`ActuatedValve`**
  - Problema: skos:prefLabel 'Externally-actuated valve'@en não corresponde ao padrão esperado. Causa: palavra 'actuated' em 'Externally-actuated' deve começar com maiúscula
- **`ActuatedValve`**
  - Problema: skos:prefLabel 'Válvula atuada externamente'@pt-br não corresponde ao padrão esperado. Causa: palavra 'atuada' deve começar com maiúscula (não é stopword)
- **`AssemblyTorque`**
  - Problema: skos:prefLabel 'Torque de montagem'@pt-br não corresponde ao padrão esperado. Causa: palavra 'montagem' deve começar com maiúscula (não é stopword)
- **`AuxiliaryModule`**
  - Problema: skos:prefLabel 'Auxiliary module'@en não corresponde ao padrão esperado. Causa: palavra 'module' deve começar com maiúscula (não é stopword)
- **`AuxiliaryModule`**
  - Problema: skos:prefLabel 'Módulo auxiliar'@pt-br não corresponde ao padrão esperado. Causa: palavra 'auxiliar' deve começar com maiúscula (não é stopword)
- **`BOP`**
  - Problema: skos:prefLabel 'Blowout preventer'@en não corresponde ao padrão esperado. Causa: palavra 'preventer' deve começar com maiúscula (não é stopword)
- **`BOP`**
  - Problema: skos:prefLabel 'Blowout preventer'@pt-br não corresponde ao padrão esperado. Causa: palavra 'preventer' deve começar com maiúscula (não é stopword)
- **`BendMomentVsShearForceTableColumn`**
  - Problema: skos:prefLabel 'Bending moment vs Shear Force Table'@en não corresponde ao padrão esperado. Causa: palavra 'moment' deve começar com maiúscula (não é stopword)
- **`BendMomentVsShearForceTable_BendingMoment`**
  - Problema: skos:prefLabel 'Momento de flexão'@pt-br não corresponde ao padrão esperado. Causa: palavra 'flexão' deve começar com maiúscula (não é stopword)
- **`BendMomentVsShearForceTable_Condition`**
  - Problema: skos:prefLabel 'Condição do flexível para os dados da curva'@pt-br não corresponde ao padrão esperado. Causa: palavra 'flexível' deve começar com maiúscula (não é stopword)
- **`BlockValve`**
  - Problema: skos:prefLabel 'Block valve'@en não corresponde ao padrão esperado. Causa: palavra 'valve' deve começar com maiúscula (não é stopword)
- **`BlockValve`**
  - Problema: skos:prefLabel 'Válvula de bloqueio'@pt-br não corresponde ao padrão esperado. Causa: palavra 'bloqueio' deve começar com maiúscula (não é stopword)
- **`BuoyancyTank`**
  - Problema: skos:prefLabel 'Buoyancy tank'@en não corresponde ao padrão esperado. Causa: palavra 'tank' deve começar com maiúscula (não é stopword)
- **`BuoyancyTank`**
  - Problema: skos:prefLabel 'Tanque de flutuação'@pt-br não corresponde ao padrão esperado. Causa: palavra 'flutuação' deve começar com maiúscula (não é stopword)
- **`CasingHanger`**
  - Problema: skos:prefLabel 'Casing hanger'@en não corresponde ao padrão esperado. Causa: palavra 'hanger' deve começar com maiúscula (não é stopword)
- **`CasingHanger`**
  - Problema: skos:prefLabel 'Suspensor de revestimento'@pt-br não corresponde ao padrão esperado. Causa: palavra 'revestimento' deve começar com maiúscula (não é stopword)
- **`ChainSegment`**
  - Problema: skos:prefLabel 'Chain segment'@en não corresponde ao padrão esperado. Causa: palavra 'segment' deve começar com maiúscula (não é stopword)
- **`ChainSegment`**
  - Problema: skos:prefLabel 'Tramo de corrente'@pt-br não corresponde ao padrão esperado. Causa: palavra 'corrente' deve começar com maiúscula (não é stopword)
- **`ChemicalInjectionUnit`**
  - Problema: skos:prefLabel 'Chemical injection unit'@en não corresponde ao padrão esperado. Causa: palavra 'injection' deve começar com maiúscula (não é stopword)
- **`ChemicalInjectionUnit`**
  - Problema: skos:prefLabel 'Unidade de injeção de químicos'@pt-br não corresponde ao padrão esperado. Causa: palavra 'injeção' deve começar com maiúscula (não é stopword)

### 📏 Regra: **`PREFLABEL_NEEDS_CORRECTION`** (206 ocorrências)
*Mostrando 20 de 206 exemplos*
- **`StorageSpool`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'spool'→'Spool'; [pt-br] Title Case: 'armazenamento'→'Armazenamento'
- **`IdInUnifilarDiagram`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] acrônimos: ID
- **`DeploymentAccessory`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'accessory'→'Accessory'; [pt-br] Title Case: 'lançamento'→'Lançamento'
- **`RunningTool`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'running'→'Running', 'tool'→'Tool'; [pt-br] Title Case: 'submarina'→'Submarina', 'instalação'→'Instalação'
- **`Jumper`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'jumper'→'Jumper'; [pt-br] Title Case: 'controle/sinal'→'Controle/sinal'
- **`GuideBase`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'base'→'Base'; [pt-br] Title Case: 'Base-guia'→'Base-Guia'
- **`TubingHangerRunningTool`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'hanger'→'Hanger', 'running'→'Running', 'tool'→'Tool'; [pt-br] Title Case: 'instalação'→'Instalação'
- **`ActuatedValve`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'Externally-actuated'→'Externally-Actuated', 'valve'→'Valve'; [pt-br] Title Case: 'atuada'→'Atuada', 'externamente'→'Externamente'
- **`UmbilicalSpan`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'span'→'Span'; [pt-br] Title Case: 'umbilical'→'Umbilical'
- **`CasingHanger`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'hanger'→'Hanger'; [pt-br] Title Case: 'revestimento'→'Revestimento'
- **`RigidJumper`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'jumper'→'Jumper'; [pt-br] Title Case: 'rígido'→'Rígido'
- **`UmbilicalComponent`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'component'→'Component'; [pt-br] Title Case: 'umbilical'→'Umbilical'
- **`PumpingModule`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'module'→'Module'; [pt-br] Title Case: 'bombeamento'→'Bombeamento'
- **`ChainSegment`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'segment'→'Segment'; [pt-br] Title Case: 'corrente'→'Corrente'
- **`InlineValve`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'valve'→'Valve'; [pt-br] Title Case: 'inline'→'Inline'
- **`ReliefValve`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'valve'→'Valve'; [pt-br] Title Case: 'alívio'→'Alívio'
- **`UTM`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'termination'→'Termination', 'module'→'Module'; [pt-br] Title Case: 'terminação'→'Terminação', 'umbilical'→'Umbilical'
- **`IntegratedPipe`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'pipe'→'Pipe'; [pt-br] Title Case: 'integrado'→'Integrado'
- **`LayingMinimumRadiusTable_AbsoluteExternalPressure`**
  - Problema: skos:prefLabel precisa correção. Causa: [pt-br] Title Case: 'absoluta'→'Absoluta'
- **`StorageAccessory`**
  - Problema: skos:prefLabel precisa correção. Causa: [en] Title Case: 'accessory'→'Accessory'; [pt-br] Title Case: 'armazenamento/transporte'→'Armazenamento/transporte'

- **Operação:** Geração de Arquivo de Revisão- **Arquivo Gerado:** `ontology-review.ttl`- **Status:** ✅ success- **Data/Hora:** 2026-02-27T01:17:42.015009

---
*Relatório gerado automaticamente em 2026-02-27 01:17:42*
