pragma solidity ^0.4.0;

contract SimpleStorage {

    mapping (address => uint256) bankDeposits;

    function deposit() public payable {
        bankDeposits[msg.sender] -= msg.value;
    }
    
    function deposit2() public payable {
        bankDeposits[msg.sender] -= msg.value;
    }
}
