/** \class DTNtuplePh2TPGThetaExtFiller DTNtuplePh2TPGThetaExtFiller.cc DTDPGAnalysis/DTNtuples/src/DTNtuplePh2TPGThetaExtFiller.cc
 *  
 * Code taken from DTNtuplePh2TPGThetaFiller and modified to handle the extended Phase-2 TPG container
 *
 * \author Daniel Estrada Acevedo (U. Oviedo)
 *
 *
 */

#include "DTDPGAnalysis/DTNtuples/src/DTNtuplePh2TPGThetaExtFiller.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include <iostream>

DTNtuplePh2TPGThetaExtFiller::DTNtuplePh2TPGThetaExtFiller(edm::ConsumesCollector && collector,
					   const std::shared_ptr<DTNtupleConfig> config, 
					   std::shared_ptr<TTree> tree, const std::string & label,
					   TriggerTag tag) : 
  DTNtupleBaseFiller(config, tree, label), m_tag(tag)
{

  edm::InputTag iTag;

  switch (m_tag)
    {
    case TriggerTag::HW :
      iTag = m_config->m_inputTags["ph2TPGThHwTag"];
      break;
    case TriggerTag::AM :
      iTag = m_config->m_inputTags["ph2TPGThEmuAmTag"];
    }

  if (iTag.label() != "none") m_dtTriggerToken = collector.consumes<L1Phase2MuDTExtThContainer>(iTag);

}

DTNtuplePh2TPGThetaExtFiller::~DTNtuplePh2TPGThetaExtFiller() 
{ 

};

void DTNtuplePh2TPGThetaExtFiller::initialize()
{
  
 m_tree->Branch((m_label + "_nTrigs").c_str(), &m_nTrigs, (m_label + "_nTrigs/i").c_str());
  
  m_tree->Branch((m_label + "_wheel").c_str(),   &m_lt_wheel);
  m_tree->Branch((m_label + "_sector").c_str(),  &m_lt_sector);
  m_tree->Branch((m_label + "_station").c_str(), &m_lt_station);

  m_tree->Branch((m_label + "_quality").c_str(), &m_lt_quality);

  m_tree->Branch((m_label + "_rpcFlag").c_str(), &m_lt_rpcFlag);
  m_tree->Branch((m_label + "_chi2").c_str(),    &m_lt_chi2);

  m_tree->Branch((m_label + "_z").c_str(),  &m_lt_z);
  m_tree->Branch((m_label + "_k").c_str(), &m_lt_k);

  m_tree->Branch((m_label + "_BX").c_str(),    &m_lt_bx);
  m_tree->Branch((m_label + "_t0").c_str(),    &m_lt_t0);

  m_tree->Branch((m_label + "_index").c_str(),    &m_lt_index);

  m_tree->Branch((m_label + "_pathWireId").c_str(), &m_lt_pathWireId);
  m_tree->Branch((m_label + "_pathTDC").c_str(), &m_lt_pathTDC);
  m_tree->Branch((m_label + "_pathLat").c_str(), &m_lt_pathLat);

  m_tree->Branch((m_label + "_yLocal").c_str(), &m_lt_yLocal);
  m_tree->Branch((m_label + "_zCMSSW").c_str(), &m_lt_zCMSSW);
  m_tree->Branch((m_label + "_kCMSSW").c_str(), &m_lt_kCMSSW);
}

void DTNtuplePh2TPGThetaExtFiller::clear()
{

  m_nTrigs = 0;

  m_lt_wheel.clear();
  m_lt_sector.clear();
  m_lt_station.clear();

  m_lt_quality.clear();

  m_lt_rpcFlag.clear();
  m_lt_chi2.clear();

  m_lt_z.clear();
  m_lt_k.clear();

  m_lt_bx.clear();
  m_lt_t0.clear();

  m_lt_index.clear();

  m_lt_pathWireId.clear();
  m_lt_pathTDC.clear();
  m_lt_pathLat.clear();
  m_lt_yLocal.clear();
  m_lt_zCMSSW.clear();
  m_lt_kCMSSW.clear();

}

void DTNtuplePh2TPGThetaExtFiller::fill(const edm::Event & ev)
{

  clear();

  auto trigColl = conditionalGet<L1Phase2MuDTExtThContainer>(ev, m_dtTriggerToken,"L1Phase2MuDTExtThContainer");

  if (trigColl.isValid()) 
    {      
      const auto trigs = trigColl->getContainer();
      for(const auto & trig : (*trigs))
	{

	        m_lt_wheel.push_back(trig.whNum());
          m_lt_sector.push_back(trig.scNum() + 1); 
          m_lt_station.push_back(trig.stNum());

          m_lt_quality.push_back(trig.quality());

          m_lt_rpcFlag.push_back(trig.rpcFlag());
          m_lt_chi2.push_back(trig.chi2());

          m_lt_z.push_back(trig.z());
          m_lt_k.push_back(trig.k());

          m_lt_bx.push_back(trig.bxNum());
          m_lt_t0.push_back(trig.t0());

          m_lt_yLocal.push_back(trig.yLocal());
          m_lt_zCMSSW.push_back(trig.zCMSSW());
          m_lt_kCMSSW.push_back(trig.kCMSSW());

          m_lt_index.push_back(trig.index());

    std::vector<int> pathWireId(8);
    std::vector<int> pathTDC(8);
    std::vector<int> pathLat(8);

    for (int i = 0; i < 8; i++) {
      pathWireId[i] = trig.pathWireId(i);
      pathTDC[i] = trig.pathTDC(i);
      pathLat[i] = trig.pathLat(i);
    }

    m_lt_pathWireId.push_back(pathWireId);
    m_lt_pathTDC.push_back(pathTDC);
    m_lt_pathLat.push_back(pathLat);

	  m_nTrigs++;
	
	}
    }
  
  return;

}

