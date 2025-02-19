#ifndef DTNtuple_DTNtuplePh2ShowerFiller_h
#define DTNtuple_DTNtuplePh2ShowerFiller_h

/** \class DTNtuplePh2ShowerFiller DTNtuplePh2ShowerFiller.h DTDPGAnalysis/DTNtuples/src/DTNtuplePh2ShowerFiller.h
 *  
 * Helper class : the Phase-1 local trigger filler for TwinMux in/out and BMTF in (the DataFormat is the same)
 *
 * \author C. Battilana (INFN BO)
 *
 *
 */

#include "DTDPGAnalysis/DTNtuples/src/DTNtupleBaseFiller.h"

#include "DataFormats/L1DTTrackFinder/interface/L1Phase2MuDTShowerContainer.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"

#include <vector>

class DTNtuplePh2ShowerFiller : public DTNtupleBaseFiller
{

 public:

  enum class TriggerTag { Ph2Sh = 0 };
  /// Constructor
  DTNtuplePh2ShowerFiller(edm::ConsumesCollector && collector,
			     const std::shared_ptr<DTNtupleConfig> config, 
			     std::shared_ptr<TTree> tree, const std::string & label, 
			     TriggerTag tag);

  ///Destructor
  virtual ~DTNtuplePh2ShowerFiller();
 
  /// Intialize function : setup tree branches etc ... 
  virtual void initialize() final;
  
  /// Clear branches before event filling 
  virtual void clear() final;

  /// Fill tree branches for a given events
  virtual void fill(const edm::Event & ev) final;    

 private :
  /// Enum to activate "flavour-by-flavour"
  /// changes in the filling logic
  TriggerTag m_tag;

  /// The shower token
  edm::EDGetTokenT<L1Phase2MuDTShowerContainer> m_dtShowerToken;

  std::vector<short> m_wheel;   // wheel (short in [-2:2] range)
  std::vector<short> m_sector;  // sector (short in [1:12] range)
  std::vector<short> m_station; // station (short in [1:4] range)
  std::vector<int> m_ndigis;    // BX : (short with a given range)
  std::vector<int> m_bx;        // BX : (short with a given range)
  std::vector<int> m_min_wire;  // Min wire
  std::vector<int> m_max_wire;  // Max wire
  std::vector<float> m_avg_pos;
  std::vector<float> m_avg_time;

};
  
#endif

