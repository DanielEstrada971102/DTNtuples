#ifndef DTNtuple_DTNtuplePh2TPGThetaExtFiller_h
#define DTNtuple_DTNtuplePh2TPGThetaExtFiller_h

/** \class DTNtuplePh2TPGThetaExtFiller DTNtuplePh2TPGThetaExtFiller.h DTDPGAnalysis/DTNtuples/src/DTNtuplePh2TPGThetaExtFiller.h
 *  
 * Code taken from DTNtuplePh2TPGThetaFiller and modified to handle the extended Phase-2 TPG container
 *
 * \author Daniel Estrada Acevedo (U. Oviedo)
 *
 *
 */

#include "DTDPGAnalysis/DTNtuples/src/DTNtupleBaseFiller.h"

#include "DataFormats/L1DTTrackFinder/interface/L1Phase2MuDTExtThContainer.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"

#include <vector>

class DTNtuplePh2TPGThetaExtFiller : public DTNtupleBaseFiller
{

 public:

  enum class TriggerTag { HW = 0, AM };

  /// Constructor
  DTNtuplePh2TPGThetaExtFiller(edm::ConsumesCollector && collector,
			     const std::shared_ptr<DTNtupleConfig> config, 
			     std::shared_ptr<TTree> tree, const std::string & label, 
			     TriggerTag tag);

  ///Destructor
  virtual ~DTNtuplePh2TPGThetaExtFiller();
 
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

  /// The digi token
  edm::EDGetTokenT<L1Phase2MuDTExtThContainer> m_dtTriggerToken;

  /// The variables holding
  /// all digi related information

  unsigned int m_nTrigs; // the # of digis (size of all following vectors)

  std::vector<short> m_lt_wheel;   // wheel (short in [-2:2] range)
  std::vector<short> m_lt_sector;  // sector (short in [1:12] range)
  std::vector<short> m_lt_station; // station (short in [1:4] range)

  std::vector<short> m_lt_quality; // quality (short in [X:Y] range)
                                   // ... // CB to be defined

  std::vector<int> m_lt_chi2; // chi2 (int in [X:Y] range)
                              // ... // CB to be defined

  std::vector<short> m_lt_rpcFlag; // quality (short in [X:Y] range)
                                   // ... // CB to be defined

  std::vector<int> m_lt_z;    // z : (int with a given scale, cm units)
                              // 65536 corresponds to 1500
  std::vector<int> m_lt_k;    // k bending : (int with a given scale, dimensionless)
                              // 65536 corresponds to 2

  std::vector<int> m_lt_bx;  // BX : (short with a given range)
                             // ... // CB to be defined
  std::vector<int> m_lt_t0;  // t0 - time with sub BX precision: 
                             // (int with a given scale) // CB to be defined

  std::vector<short> m_lt_index; // index : (short in [X:Y] range) 
                                 // tags multiple primitives per chamber per BX
                                 // ... // CB to be defined
 std::vector<std::vector<int>> m_lt_pathWireId; // wireId of the 8 hits composing the segment
 std::vector<std::vector<int>> m_lt_pathTDC;    // TDC of the 8 hits composing the segment
 std::vector<std::vector<int>> m_lt_pathLat;   // Laterality of the 8 hits composing the segment

 std::vector<int> m_lt_yLocal; // y position in local directly from the Trigger Primitive
 std::vector<int> m_lt_zCMSSW; // z position in local directly from the Trigger Primitive
 std::vector<int> m_lt_kCMSSW; // k bending in local directly from the Trigger Primitive
};
  
#endif
