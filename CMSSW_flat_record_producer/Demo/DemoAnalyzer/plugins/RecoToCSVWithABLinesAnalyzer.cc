
/****************************************************************************
 *
 * This is a part of TOTEM offline software.
 * Authors:
 *   Patryk Ławski (patryk.jakub.lawski@cern.ch, patryk.lawski@gmail.com)
 *
 ****************************************************************************/


#include "Demo/DemoAnalyzer/interface/DemoAnalyzer.h"
#include "Demo/DemoAnalyzer/interface/RecoToCSVWithABLinesAnalyzer.h"


RecoToCSVWithABLinesAnalyzer::RecoToCSVWithABLinesAnalyzer(const edm::ParameterSet& ps)
{
  std::string fillFileName = ps.getParameter<std::string>("fill_file_name");
  
  row_counter = 0;
  recoId = ps.getParameter<std::string>("recoId");
  linesCSV.open(fillFileName);
  linesCSV << "recoID,eventID,armID,groupID,rpID,uLineSize,vLineSize,siliconID,position,sigma_,uv_line_a,uv_line_b,uv_line_w\n";  
}

RecoToCSVWithABLinesAnalyzer::~RecoToCSVWithABLinesAnalyzer(){
  linesCSV.close();
}


void 
RecoToCSVWithABLinesAnalyzer::hits_log(int eventID, std::string &direction, unsigned int uLineSize, unsigned int vLineSize, RPRecognizedPatterns::Line &line) {
  
  std::vector<RPRecoHit> hits = line.hits;
  unsigned int totalHitsNumber = hits.size();

  // Prepare line related data
  unsigned int rawDetId = hits[0].DetId();
  unsigned int armID = armId(rawDetId);
  unsigned int groupID = getSingleGroupId(rawDetId);
  unsigned int rpID = pureRpId(rawDetId);
  

  for(unsigned int hit_no = 0; hit_no < totalHitsNumber; hit_no++) {
      RPRecoHit curr_hit = hits[hit_no];

      unsigned int currRawDetId = curr_hit.DetId();
      unsigned int siliconID = siliconId(currRawDetId);

      linesCSV  << recoId << ","
                << eventID << ","
                << armID << ","
                << groupID << ","
                << rpID << ","
                << uLineSize << ","
                << vLineSize << ","
                << siliconID << ","
                << curr_hit.Position() << ","
                << curr_hit.Sigma() << ","
                << line.a << ","
                << line.b << ","
                << line.w << "\n";
  }
}


void 
RecoToCSVWithABLinesAnalyzer::lines_log(std::vector<RPRecognizedPatterns::Line> &lines, std::string &direction, int eventId, unsigned int uLinesNumber, unsigned int vLinesNumber){
  
  unsigned int totalLineNumber = lines.size();
  RPRecognizedPatterns::Line curr_line;

  for(unsigned int line_no = 0; line_no < totalLineNumber; line_no++){
    curr_line = lines[line_no];
  
    hits_log(eventId, direction, uLinesNumber, vLinesNumber, curr_line);    
  }
}

// ------------ method called for each event  ------------
void
RecoToCSVWithABLinesAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  using namespace std;

  Handle<RPRecognizedPatternsCollection> input;
  iEvent.getByLabel("NonParallelTrackFinder", input);

  int eventId = iEvent.id().event();

  for (auto it : *input)
  {
    unsigned int uLinesNumber = it.second.uLines.size();
    unsigned int vLinesNumber = it.second.vLines.size();
    
    if(uLinesNumber == 1 && vLinesNumber == 1){     // CONDITION ONLY SINGLE TRACKING --> zastanowiłbym się nad tym warunkiem....
      // lines to CSV
      string direction = "u";
      lines_log(it.second.uLines, direction, eventId, uLinesNumber, vLinesNumber);
      direction = "v";
      lines_log(it.second.vLines, direction, eventId, uLinesNumber, vLinesNumber);  
    }
    
  }

#ifdef THIS_IS_AN_EVENT_EXAMPLE
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);
#endif
   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif
}


// ------------ method called once each job just before starting event loop  ------------

void 
RecoToCSVWithABLinesAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
RecoToCSVWithABLinesAnalyzer::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
RecoToCSVWithABLinesAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
RecoToCSVWithABLinesAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
RecoToCSVWithABLinesAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
RecoToCSVWithABLinesAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/


/* detector_map = {
    1 : "L-TOP", 24, 20, 4, 0
    2 : "L-BOT", 25, 21, 5, 1
    3 : "L-HOR", 23, 22, 3, 2
    
    4 : "R-TOP", 100, 104, 120, 124
    5 : "R-BOT", 101, 105, 121, 125
    6 : "R-HOR", 102, 103, 122, 123
} */

unsigned int
getSingleGroupId(unsigned int rawDetId) {

  unsigned int rp_id = pureRpId(rawDetId);
  unsigned int result = 0;



  if (rp_id % 10 == 0 || rp_id % 10 == 4) {
    result += 1;
  } else if (rp_id % 10 == 1 || rp_id % 10 == 5) {
    result += 2;
  } else {
    result += 3;
  }

  if (rp_id/100 == 1) {
    result += 3;
  }

  return result;
}


// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
RecoToCSVWithABLinesAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(RecoToCSVWithABLinesAnalyzer);