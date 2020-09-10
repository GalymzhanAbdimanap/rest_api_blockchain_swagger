// Market place (smart contract) on Tron blockchain platform.
// Copyright (c) 2020 IDET.kz
// Written by Galymzhan Abdimanap.

pragma solidity 0.5.9;
pragma experimental ABIEncoderV2;
//import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/math/SafeMath.sol";
import "SafeMath.sol";
import "Token_contract.sol";




contract AuctionBox{
    // Market place. Main contract. 
    // Functions: purchase, confirm purchase, sale of good, generate checks, good's wallet and etc. 
    using SafeMath for uint256;
    // Object of token contract.
    TRC20 trc20;
    
    
    string index_;
    uint sale_price;
    uint sale_commission;
    bool isExist;
    uint _index=0;
    
    // Address of token contract.
    uint256 add_token = 0x411576d1a39ace4f0a24fc52b7a17be97904f6a2b8;
    // State of good.
    enum State{Default, Running, Finalized}
    State public auctionState;
    
    
    
    
    // contract Auctions
    // 
    uint public count;
    address owner = msg.sender;
    uint _index_auctions=0;
    uint startPrice;
    string description;
    uint commission;
    uint constPrice;
    uint commisionConst;  
    uint public highestPrice;
    address payable public highestBidder;
    
    mapping(uint=>mapping(address => mapping(uint=>uint))) public bids;
    mapping(uint=>mapping(address => mapping(uint=>uint))) public bids_goods;
    mapping(uint=>mapping(address => uint)) public goods;
    mapping(uint=>State) public aucStates;
    
    
    function convertFromTronInt(uint256 tronAddress) public view returns(address){
      return address(tronAddress);
    }
    
    
    constructor() public{
        // address of contract tokens
        trc20 = TRC20(address(add_token));
        
        
    }
    
    struct WalletOfGood{
        string nameOfgood;
        uint amountOfgood;
        uint price;
        uint addressOfgood;
        uint commission;
    }
    
    struct ChecksOfGood{
        string[]   nameOfGood ;
        uint[]     amountOfGood; 
        uint[]     Price  ;
        uint[]     sumPrice;
        uint[]  id_auction;
        string   timestamp;
        bool     status;
        uint allSumPrice;
        string type_op;
        bool isCanceled;
    }
    
    struct Auctions{
        string  title;
        uint startPrice;
        string  description;
        uint  count;
        uint commission;
        
    }
    mapping(uint=>Auctions) AllAuctions;
    mapping(address=>mapping(uint=>WalletOfGood)) walletOfGoods;
    uint[] confirmGivenArray;
    mapping(address=>mapping(uint=>ChecksOfGood)) checksOfGood;
    mapping(address=>uint[]) addressOfGoods;
    mapping(address=>uint[]) indexesOfChecks;
    
     
   
    //_address_receipt = address of account
    function setChecksOfGoods(address _address_receipt, uint _index, string memory _nameOfgood, uint _amountOfGood,  uint _Price, uint _sumPrice, uint  _id_auction, string memory _timestamp, bool _status, string memory _type_op, bool _isCanceled) public{
        
        
        checksOfGood[_address_receipt][_index].nameOfGood.push(_nameOfgood);
        checksOfGood[_address_receipt][_index].amountOfGood.push(_amountOfGood);
        checksOfGood[_address_receipt][_index].Price.push(_Price);
        checksOfGood[_address_receipt][_index].sumPrice.push(_sumPrice);
        checksOfGood[_address_receipt][_index].id_auction.push(_id_auction);
        checksOfGood[_address_receipt][_index].timestamp = _timestamp;
        checksOfGood[_address_receipt][_index].status = _status;
        checksOfGood[_address_receipt][_index].allSumPrice = checksOfGood[_address_receipt][_index].allSumPrice.add(_sumPrice);
        checksOfGood[_address_receipt][_index].type_op = _type_op;
        checksOfGood[_address_receipt][_index].isCanceled = _isCanceled;
        //goodChecks.push(_address_receipt);
        
        
    }
    //_address_receipt = address of account
    function getChecksOfGoods(address _address_receipt, uint _index) view public returns (string [] memory, uint[] memory, uint[] memory, uint[] memory, uint[] memory, uint, string memory, bool, uint, string memory, bool){
        address _a = _address_receipt;
        uint _i = _index;
        
        return (checksOfGood[_a][_i].nameOfGood, checksOfGood[_a][_i].amountOfGood, checksOfGood[_a][_i].Price, checksOfGood[_a][_i].sumPrice, checksOfGood[_a][_i].id_auction, _i, checksOfGood[_a][_i].timestamp, checksOfGood[_a][_i].status, checksOfGood[_a][_i].allSumPrice, checksOfGood[_a][_i].type_op, checksOfGood[_a][_i].isCanceled);
        ///////
        
    }
    
   
    //_address = address of account
    function settWalletOfGoods(address _address, uint _id_auction, string memory _nameOfgood, uint _amountOfgood, uint _price, uint _commission) public{
        // Add goods in wallet.
        walletOfGoods[_address][_id_auction].nameOfgood = _nameOfgood;
        walletOfGoods[_address][_id_auction].price = _price;
        walletOfGoods[_address][_id_auction].amountOfgood += _amountOfgood;
        walletOfGoods[_address][_id_auction].addressOfgood = _id_auction;
        walletOfGoods[_address][_id_auction].commission = _commission;
    }
    
    //_address = address of account
    function setNameOfGoodFromWallet(address _address, uint _id_auction) public{
        // Return names of good from user's wallet.
        isExist=false;
        for(uint i=0; i<addressOfGoods[_address].length; i++){
            
            if(addressOfGoods[_address][i]==_id_auction){
                isExist=true;
            }
        }
        if (isExist==false){
             addressOfGoods[_address].push(_id_auction);
             
        }
    }
    
    //_address = address of account
    function setIndexOfChecks(address _address, uint _index)public{
        // Add ID of user's check in db.
        indexesOfChecks[_address].push(_index);
    }

    function setIsConfirmGiven(address _address, uint _index) public{
        // Change status of purchase on success.
        checksOfGood[_address][_index].status = true;
    }
    
    function setIsCancelOfPurchase(address _address, uint _index) public{
        // Change status of purchase on failed.
        checksOfGood[_address][_index].isCanceled = true;
    }
    
    //_address = address of account
    function getAddressOfGoodFromWallet(address _address) view public returns (uint[] memory){
        // Return ids of users from wallet.
        return (addressOfGoods[_address]);
    }
    
    //_address = address of account
    function getIndexOfChecksAndIsConfirm(address _address) view public returns(uint[] memory){
        // Return ids of user's checks.
        return indexesOfChecks[_address];
    }
    
    
    function getWalletOfGood_array(address _address, uint _id_auction) view public returns (string memory, uint,uint, uint, uint){
        // Return info about goods from user's wallet.
        return (walletOfGoods[_address][_id_auction].nameOfgood, walletOfGoods[_address][_id_auction].amountOfgood,walletOfGoods[_address][_id_auction].price, walletOfGoods[_address][_id_auction].addressOfgood, walletOfGoods[_address][_id_auction].commission);   
    }

   function saleOfGoods(uint _id_auction, uint _amountOfgood, uint id, string memory tmstp) public{
       // Sale users's goods.
       require(_amountOfgood<=walletOfGoods[msg.sender][_id_auction].amountOfgood);
       
        string memory ttl = returnTitleAuctions(_id_auction);
        uint strtPrc = returnStrtPrcAuctions(_id_auction);
        uint cnt = returnCountAuctions(_id_auction);
        uint commission = returnCommissionAuctions(_id_auction);
        uint cnstPrc;
        cnstPrc = strtPrc;
        uint id_a = _id_auction; 
       // Connect with token contract.
       trc20 = TRC20(address(0x411576d1a39ace4f0a24fc52b7a17be97904f6a2b8));
       // Add amount of goods from sale on market place.
       setCountAdd(_id_auction, _amountOfgood);
       // Delete saled amount of goods from users's wallet.
       walletOfGoods[msg.sender][_id_auction].amountOfgood = walletOfGoods[msg.sender][_id_auction].amountOfgood.sub(_amountOfgood);
       // Get tokens from sale with including commission
       strtPrc = walletOfGoods[msg.sender][id_a].price.mul(100000000).mul(_amountOfgood).sub(walletOfGoods[msg.sender][id_a].commission.mul(1000000).mul(_amountOfgood));
       trc20.approve(address(this), msg.sender, strtPrc);
       // Move to tokens to contract address
       trc20.transfer(msg.sender,strtPrc);
       setChecksOfGoods(msg.sender, id, ttl, _amountOfgood, cnstPrc, strtPrc.div(100000000), id_a, tmstp, true, "sale", false);
       //
       if(walletOfGoods[msg.sender][_id_auction].amountOfgood==0){
           for(uint i=0; i<addressOfGoods[msg.sender].length; i++){
            if(addressOfGoods[msg.sender][i]==_id_auction){
                delete addressOfGoods[msg.sender][i];
            }
        }
       }
       
   }
   
   //_addresses = address Of goods
   function saleOfGoodsBox(uint[] memory _amountOfgoods, uint[] memory _id_auctions, string memory _timestamp)public {
       // Accept multi sale.
       _index = addIndex();
       
       for(uint i=0; i<_id_auctions.length; i++){
          saleOfGoods(_id_auctions[i], _amountOfgoods[i], _index, _timestamp);
           
       }
       setIndexOfChecks(msg.sender, _index);
   }
  
   function placeBidBox(uint[] memory _id_auctions, uint[] memory _amounts, string memory _timestamp)public{
       // Accept multi purchase.
       _index = addIndex();
       
       for(uint i=0; i<_id_auctions.length; i++){
           //a = Auction(address(_addresses[i]));
           placeBid(_id_auctions[i], _amounts[i], msg.sender, _timestamp, _index);
           
       }
       setIndexOfChecks(msg.sender, _index);

   }
   
   function finalizeBox(uint[] memory _id_auctions, uint _index)public{
       // Confirm purchase.
        for(uint i=0; i<_id_auctions.length; i++){
            //a = Auction(address(_addresses[i]));
            finalizeAuction(_id_auctions[i], msg.sender, _index);
   }
   }
   
   //addresses = addresses auction
   function cancelConfirmBox(uint[] memory _id_auctions, uint  _index)public{
       // Accept multi confirm.
       for(uint i=0; i<_id_auctions.length; i++){
            cancelConfirm(_id_auctions[i],msg.sender, _index);
       }
   }
   
   function balanceOf(address account)  external view returns(uint256){
        // Return balance of user in token contract.
        uint256 balance = trc20.balanceOf(account);
        return balance;
    }
    
    function addIndex() public returns(uint){
        // Add index of checks.
        return _index+=1;
    }
   
    
    function createAuction(
        // Create good for market place.
        string memory _title,
        uint _startPrice,
        string memory _description,
        uint  _count,
        uint _commission) payable public{
            AllAuctions[_index_auctions].title = _title;
            AllAuctions[_index_auctions].startPrice = _startPrice;
            AllAuctions[_index_auctions].description = _description;
            AllAuctions[_index_auctions].count = _count;
            AllAuctions[_index_auctions].commission = _commission;
            aucStates[_index_auctions] = State.Running;
            _index_auctions+=1;
            
            
        }
    function returnContentsAuctions(uint _index_auctions)public view returns(uint, string memory, uint, string memory, uint, uint){
        // Return content of good.
        return (_index_auctions, AllAuctions[_index_auctions].title, AllAuctions[_index_auctions].startPrice, AllAuctions[_index_auctions].description, AllAuctions[_index_auctions].count, AllAuctions[_index_auctions].commission);
    }
        
    function returnTitleAuctions(uint _index_auctions)public view returns(string memory){
        return AllAuctions[_index_auctions].title;
        
    }
    function returnStrtPrcAuctions(uint _index_auctions)public view returns(uint){
        return AllAuctions[_index_auctions].startPrice;
        
    }
    function returnCountAuctions(uint _index_auctions)public view returns(uint){
        return AllAuctions[_index_auctions].count;
        
    }
    function returnCommissionAuctions(uint _index_auctions)public view returns(uint){
        return AllAuctions[_index_auctions].commission;  
    }
  
    function getIndexAuctions()public view returns(uint){
        return _index_auctions;
    }

    modifier notOwner(){
        require(msg.sender != owner);
        _;
    }

    function setCountAdd(uint _id_auc, uint _count) public {
        AllAuctions[_id_auc].count = AllAuctions[_id_auc].count.add(_count);   
    }
    
    function setCountSub(uint _id_auc, uint _count) public {
        AllAuctions[_id_auc].count = AllAuctions[_id_auc].count.sub(_count);   
    }

    // buy goods
    function placeBid(uint _id_auctions, uint amt, address addr, string memory tmstp, uint id)  public notOwner returns(bool) {
        // Accept buy goods.
        string memory ttl = returnTitleAuctions(_id_auctions);
        uint strtPrc = returnStrtPrcAuctions(_id_auctions);
        uint cnt = returnCountAuctions(_id_auctions);
        uint commission = returnCommissionAuctions(_id_auctions);
        uint cnstPrc;
        cnstPrc = strtPrc;
        uint id_a = _id_auctions;
        string memory time = tmstp;
        
        
        require(aucStates[id_a] == State.Running);
        require(cnt>=amt);
       
              
        goods[id_a][addr] = goods[id_a][addr].add(amt);
        
        strtPrc = strtPrc.mul(100000000).mul(amt).add(commission.mul(1000000).mul(strtPrc).mul(amt));
        
        //strtPrc = strtPrc.mul(amt).add(commission.mul(cnstPrc).div(100).mul(amt));
        
        bids[id_a][addr][id] = bids[id_a][addr][id].add(strtPrc);
        
        bids_goods[id_a][addr][id] = bids_goods[id_a][addr][id].add(amt);
        
        trc20.approve(addr, address(this), strtPrc);
        
        // Move to tokens to contract address
        trc20.transferFrom(addr, address(this), strtPrc);
        
        setCountSub(_id_auctions, amt);

        setChecksOfGoods(addr, id, ttl, amt, cnstPrc, strtPrc.div(100000000), id_a, time, false, "purchase", false);
        
        //setChecksOfGoods(addr, id, ttl, amt, cnstPrc, strtPrc, address(this), tmstp, false, "purchase");
        
        
        
        //startPrice=constPrice;
        
        return true;
}

    
     function finalizeAuction(uint _id_auctions, address _address, uint _index) payable public{
        //confirm given good
        string memory ttl = returnTitleAuctions(_id_auctions);
        uint strtPrc = returnStrtPrcAuctions(_id_auctions);
        uint cnt = returnCountAuctions(_id_auctions);
        uint cmsn = returnCommissionAuctions(_id_auctions);
        uint cnstPrc;
        cnstPrc = strtPrc;
         
        //the owner and bidders can finalize the auction.
        require(_address == owner || bids[_id_auctions][_address][_index] > 0);
        
        address payable recipiant;
        uint value;
        
        // owner can get highestPrice
        if(_address == owner){
            value = 0;
            
        }
    
        // Other bidders can get back the money 
        else {
            value =  bids[_id_auctions][_address][_index];
        }
        // initialize the value
        bids[_id_auctions][_address][_index] = 0;
        //recipiant.transfer(value);
        setNameOfGoodFromWallet(_address, _id_auctions);
        
        settWalletOfGoods(_address, _id_auctions, ttl, bids_goods[_id_auctions][_address][_index], cnstPrc, cmsn);
        
        trc20.approve(address(this), owner, value);
        
        trc20.transfer(owner, value);
        
        setIsConfirmGiven(_address, _index);
        
        if(cnt<=0){
            aucStates[_id_auctions] = State.Finalized;
        }
        
    }
    
    function cancelConfirm(uint _id_auctions, address _address, uint _index) payable public{
        require(_address == owner || bids[_id_auctions][_address][_index] > 0);
        
        address payable recipiant;
        uint value;
        
        // owner can get highestPrice
        if(_address == owner){
            value = 0;
            
        }
    
        // Other bidders can get back the money 
        else {
            value =  bids[_id_auctions][_address][_index];
        }
        // initialize the value
        bids[_id_auctions][_address][_index] = 0;
        //recipiant.transfer(value);
        trc20.approve(address(this), _address, value);
        
        trc20.transfer(_address, value);
        
        setIsCancelOfPurchase(_address, _index);
        
        
    }
    
    
    
    
    
}






