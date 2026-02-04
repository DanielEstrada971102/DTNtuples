/** \class DTNtuplePh2TPGPhiExtFiller DTNtuplePh2TPGPhiExtFiller.cc DTDPGAnalysis/DTNtuples/src/DTNtuplePh2TPGPhiExtFiller.cc
 *  
 * Code taken from DTNtuplePh2TPGPhiFiller and modified to handle the extended Phase-2 TPG container
 *
 * \author Daniel Estrada Acevedo (U. Oviedo)
 *
 *
 */

#include "DTDPGAnalysis/DTNtuples/src/DTNtuplePh2TPGPhiExtFiller.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include <iostream>

DTNtuplePh2TPGPhiExtFiller::DTNtuplePh2TPGPhiExtFiller(edm::ConsumesCollector && collector,
					   const std::shared_ptr<DTNtupleConfig> config, 
					   std::shared_ptr<TTree> tree, const std::string & label,
					   TriggerTag tag) : 
  DTNtupleBaseFiller(config, tree, label), m_tag(tag)
{

  edm::InputTag iTag;

  switch (m_tag)
    {
    case TriggerTag::HW :
      iTag = m_config->m_inputTags["ph2TPGPhiHwTag"];
      break;
    case TriggerTag::HB :
      iTag = m_config->m_inputTags["ph2TPGPhiEmuHbTag"];
      break;
    case TriggerTag::AM :
      iTag = m_config->m_inputTags["ph2TPGPhiEmuAmTag"];
    }

  if (iTag.label() != "none") m_dtTriggerToken = collector.consumes<L1Phase2MuDTExtPhContainer>(iTag);

}

DTNtuplePh2TPGPhiExtFiller::~DTNtuplePh2TPGPhiExtFiller() 
{ 

};

void DTNtuplePh2TPGPhiExtFiller::initialize()
{
  
  m_tree->Branch((m_label + "_nTrigs").c_str(), &m_nTrigs, (m_label + "_nTrigs/i").c_str());
  
  m_tree->Branch((m_label + "_wheel").c_str(),   &m_lt_wheel);
  m_tree->Branch((m_label + "_sector").c_str(),  &m_lt_sector);
  m_tree->Branch((m_label + "_station").c_str(), &m_lt_station);

  m_tree->Branch((m_label + "_quality").c_str(), &m_lt_quality);
  m_tree->Branch((m_label + "_superLayer").c_str(), &m_lt_superLayer);

  m_tree->Branch((m_label + "_rpcFlag").c_str(), &m_lt_rpcFlag);
  m_tree->Branch((m_label + "_chi2").c_str(),    &m_lt_chi2);

  m_tree->Branch((m_label + "_phi").c_str(),  &m_lt_phi);
  m_tree->Branch((m_label + "_phiB").c_str(), &m_lt_phiB);

  m_tree->Branch((m_label + "_posLoc_x").c_str(),  &m_lt_posLoc_x);
  m_tree->Branch((m_label + "_dirLoc_phi").c_str(), &m_lt_dirLoc_phi);

  m_tree->Branch((m_label + "_BX").c_str(),    &m_lt_bx);
  m_tree->Branch((m_label + "_t0").c_str(),    &m_lt_t0);

  m_tree->Branch((m_label + "_index").c_str(),    &m_lt_index);

  m_tree->Branch((m_label + "_pathWireId").c_str(), &m_lt_pathWireId);
  m_tree->Branch((m_label + "_pathTDC").c_str(), &m_lt_pathTDC);
  m_tree->Branch((m_label + "_pathLat").c_str(), &m_lt_pathLat);

  m_tree->Branch((m_label + "_xLocal").c_str(), &m_lt_xLocal);
  m_tree->Branch((m_label + "_tanPsi").c_str(), &m_lt_tanPsi);
  m_tree->Branch((m_label + "_phiCMSSW").c_str(), &m_lt_phiCMSSW);
  m_tree->Branch((m_label + "_phiBCMSSW").c_str(), &m_lt_phiBCMSSW);
}

void DTNtuplePh2TPGPhiExtFiller::clear()
{

  m_nTrigs = 0;

  m_lt_wheel.clear();
  m_lt_sector.clear();
  m_lt_station.clear();

  m_lt_quality.clear();
  m_lt_superLayer.clear();

  m_lt_rpcFlag.clear();
  m_lt_chi2.clear();

  m_lt_phi.clear();
  m_lt_phiB.clear();

  m_lt_posLoc_x.clear();
  m_lt_dirLoc_phi.clear();

  m_lt_bx.clear();
  m_lt_t0.clear();

  m_lt_index.clear();

  m_lt_pathWireId.clear();
  m_lt_pathTDC.clear();
  m_lt_pathLat.clear();

  m_lt_xLocal.clear();
  m_lt_tanPsi.clear();
  m_lt_phiCMSSW.clear();
  m_lt_phiBCMSSW.clear();

}

void DTNtuplePh2TPGPhiExtFiller::fill(const edm::Event & ev)
{

  clear();

  auto trigColl = conditionalGet<L1Phase2MuDTExtPhContainer>(ev, m_dtTriggerToken,"L1Phase2MuDTExtPhContainer");

  if (trigColl.isValid()) 
    {      
      const auto trigs = trigColl->getContainer();
      for(const auto & trig : (*trigs))
	{

	  m_lt_wheel.push_back(trig.whNum());
	  m_lt_sector.push_back(trig.scNum() + 1); 
	  m_lt_station.push_back(trig.stNum());
	  
	  m_lt_quality.push_back(trig.quality());
	  m_lt_superLayer.push_back(trig.slNum());

	  m_lt_rpcFlag.push_back(trig.rpcFlag());
	  m_lt_chi2.push_back(trig.chi2());

	  m_lt_phi.push_back(trig.phi());
	  m_lt_phiB.push_back(trig.phiBend());
	  
	  m_lt_posLoc_x.push_back(m_tag == TriggerTag::HB ? 
				  m_config->m_trigGeomUtils->trigPosCHT(&trig) :
				  m_config->m_trigGeomUtils->trigPosAM(&trig)  );
	  m_lt_dirLoc_phi.push_back(m_tag == TriggerTag::HB ? 
				    m_config->m_trigGeomUtils->trigDirCHT(&trig) :
				    m_config->m_trigGeomUtils->trigDirAM(&trig)  );

	  m_lt_bx.push_back(trig.bxNum());
	  m_lt_t0.push_back(trig.t0());

    m_lt_xLocal.push_back(trig.xLocal());
    m_lt_tanPsi.push_back(trig.tanPsi());
    m_lt_phiCMSSW.push_back(trig.phiCMSSW());
    m_lt_phiBCMSSW.push_back(trig.phiBendCMSSW());
	  
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

